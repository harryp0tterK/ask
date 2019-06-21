# [Ask](https://askme.site)

This is an implementation of a basic Question and Answer platform. It is a very typical 
[Django](https://www.djangoproject.com/) app, you may use it as a stand-alone 
web site, plug it into an existing project or somehow else. I created it for a local scientific
conference and it worked well, so If someone else needs that sort of functionality - 
here it is, almost ready... 

With this app users can create and log in to account, create/modify questions 
and answers, it has categories, tags, simple search and more.

Check out the [demo](https://askme.site). Here are credentials in a case you do not
want to create a new user: 
-  username: Robert
-  password: testuser

## Getting Started

But, to get started with the app, obviously, you will need a general understanding of how Django works. 
You will also need to set up environment variables and a database 
(do not even try SQLite in production, works smoothly with PostgreSQL).

If you want to test it locally - just start a Django project the usual way, 
copy folders and files into it, do not forget to add the 
*'users.apps.UsersConfig'* and *'qa.apps.QaConfig'* to the **INSTALLED_APPS**
of settings.py, turn on debug mode, 
install some extra apps from requirements.txt and, boom - 
you are ready to go - `./manage.py runserver.`

The easiest way to actually get this thing going in production is to push it to 
[Heroku (or Dokku)](https://devcenter.heroku.com/articles/git); anyway, I made it with Docker in mind. 

## Installing

Sorry, there will be no step-by-step manual, I assume you know what you are doing.

## Built With

-  [Django](https://www.djangoproject.com/) - The web framework used    
-  [Virtualenv](https://virtualenv.pypa.io/en/latest/)
-  [Gunicorn](https://gunicorn.org/) -  a WSGI HTTP Server
-  [Pillow](https://pillow.readthedocs.io/en/stable/)
-  [crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
-  [Bootstrap 4](https://getbootstrap.com/) - The front end library
-  [nginx](https://nginx.org/) - a reverse proxy server. 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details