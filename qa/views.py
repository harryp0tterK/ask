from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Question, Answer
from users.models import CustomUser
from .forms import AskForm, AnswerForm


def home(request, a_id=None):
    """Here we're trying to serve two urls with one view: / and popular"""

    new_questions = Question.objects.new()
    pref = ''

    if 'popular' in request.path:
        new_questions = Question.objects.popular()
        pref = '/popular/'

    if 'author' in request.path and a_id:
        # this case returns Questions by an Author chosen by an a_id
        auth = get_object_or_404(CustomUser, id=a_id)
        new_questions = auth.question_set.new()

    # let's create a paginator object
    limit = request.GET.get('limit', 10)
    page = int(request.GET.get('page', 1))
    paginator = Paginator(new_questions, limit)
    paginator.baseurl = pref + '?page='

    try:
        # try to deliver a page.
        questions = paginator.page(page)

    except EmptyPage:
        # If the page is out of range (e.g. 9999), serve the last one available.
        questions = paginator.page(paginator.num_pages)

    return render(request, 'qa/questions.html', {
        'questions': questions,
        'paginator': paginator,
    })


def question(request, qn_id):
    """this view will return a single question + related answers by id and CREATE answers"""

    qn = get_object_or_404(Question, id=qn_id)
    # list of active parent answers
    answers = qn.answer_set.filter(active=True, parent__isnull=True)
    ans_form = AnswerForm()

    if request.method == 'POST':
        # here is an answer form for the <id> question
        if request.user.is_authenticated:
            ans_form = AnswerForm(request.POST)

            if ans_form.is_valid():

                '''here is a code for replies on answers (answers with 'parents'). It works, but\
                I am not sure if i still want this feature: I'll think it over later'''

                try:  # get parent comment id from hidden input
                    parent_id = int(request.POST.get('parent_id'))
                except:  # fixme
                    parent_id = None

                if parent_id:  # if parent_id has been submitted get parent_obj id
                    parent_obj = Answer.objects.get(id=parent_id)
                    if parent_obj:  # if parent object exist
                        reply_answer = ans_form.save(commit=False)  # create reply object
                        reply_answer.parent = parent_obj  # assign parent_obj to reply
                        # end of the sub-answers code

                # normal answer
                ans_form = ans_form.save(commit=False)  # pre-save form, but won't commit changes to the DB yet
                ans_form.author = request.user
                ans_form.question = qn
                # here we are adding user and question objects to the form and finally save it to the DB
                ans_form.save()

            return redirect(qn.get_url())

        else:
            m = messages.warning(request, 'Sorry! You have to login first!')
            return redirect(f'/users/login?next={qn.get_url()}', m)

    return render(request, 'qa/question.html', {'qn': qn, 'answers': answers, 'ans_form': ans_form})


@login_required
def ask(request):
    """create new question"""

    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            m = messages.success(request, 'OK! The question was created')

            return redirect(form.get_url(), m)
    else:
        form = AskForm()

    return render(request, 'qa/askform.html', {'form': form})


@login_required
def delete(request, obj_type, o_id):
    """ this view simply deletes both Questions and Answers"""

    choose = {'q': [Question, 'question'],
              'a': [Answer, 'answer']}
    try:
        obj = get_object_or_404(choose[obj_type][0], id=o_id)
        if request.method == "POST" and obj.author == request.user:
            obj.delete()
            m = messages.success(request, f'OK! your {choose[obj_type][1]} was deleted')
            return redirect('/', m) if obj_type == 'q' else redirect(obj.question.get_url(), m)
    except (KeyError,):
        return redirect('/')


@login_required
def edit(request, obj_type, o_id):
    """this is edit view for both Questions and Answers"""

    choose = {'q': [Question, AskForm, 'qa/askform.html', 'question'],
              'a': [Answer, AnswerForm, 'qa/edit.html', 'answer']}
    try:
        obj = get_object_or_404(choose[obj_type][0], id=o_id)
        if request.method == "POST" and obj.author == request.user:
            form = choose[obj_type][1](request.POST, instance=obj)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.added_at = timezone.now()
                m = messages.success(request, f"The {choose[obj_type][3]} was successfully edited")
                obj.save()
                return redirect(obj.get_url(), m) if obj_type == 'q' else redirect(obj.question.get_url(), m)
        else:
            form = choose[obj_type][1](instance=obj)

        return render(request, choose[obj_type][2], {'form': form})

    except (KeyError,):
        raise Http404
