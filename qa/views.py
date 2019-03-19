from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from .models import Question
from .forms import AskForm, AnswerForm


def home(request):
    """Here we're trying to serve two urls with one view: / and popular"""
    new_questions = Question.objects.new()
    pref = ''

    if 'popular' in request.path:
        new_questions = Question.objects.popular()
        pref = '/popular/'
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
    """this view will return a single question + related answers by id or 404"""
    qn = get_object_or_404(Question, id=qn_id)
    answers = qn.answer_set.all()
    ans_form = AnswerForm()

    if request.method == 'POST':
        # here is an answer form for the <id> question
        if request.user.is_authenticated:
            ans_form = AnswerForm(request.POST)

            if ans_form.is_valid():
                ans_form = ans_form.save(commit=False)
                # this will pre-save form, but won't commit changes to the DB yet
                ans_form.author = request.user
                ans_form.question = qn
                # here we are adding user and question objects to the form and finally save it to DB
                ans_form.save()

            return HttpResponseRedirect(qn.get_url())

        else:
            return HttpResponseRedirect(f'/users/login?next={qn.get_url()}')

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

            return HttpResponseRedirect(form.get_url())
    else:
        form = AskForm()

    return render(request, 'qa/askform.html', {'form': form})
