from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login
from django.conf import settings

from importlib import import_module
# settings.SESSION_ENGINE default value is 'django.contrib.sessions.backends.db'
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def index(request):
    if request.user.is_authenticated():
        return HttpResponse('Hello, ' + request.user.username)
    # if user is already logined, then there is code in browser
    elif 'code' in request.GET:
        request.session = SessionStore(request.GET['code'])
        # modify session, so make user's cookie can stay longger in db
        request.session.modified = True
        return redirect(index)
    else:
        return redirect_to_login(
            request.build_absolute_uri(),
            settings.SSO_AUTH_URL, 'callback')
