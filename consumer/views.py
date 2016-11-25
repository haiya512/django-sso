# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login
from django.conf import settings

from importlib import import_module
# settings.SESSION_ENGINE default value is 'django.contrib.sessions.backends.db'
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def index(request):
    # request.session info:
    # _auth_user_hash : e4c03ceac765e6d4bf10387b5ea949e963cbfea3
    # _auth_user_id : 1
    # _auth_user_backend : django.contrib.auth.backends.ModelBackend
    if request.user.is_authenticated():
        print "is auth"
        return HttpResponse('Hello, ' + request.user.username)
    # if user is already logined, then there is code in browser
    elif 'code' in request.GET:
        print "code in get"
        # 这种情况一般会用在用户收藏URL的时候，把key也给带上了，如果没有失效则不用输密码
        # 就可以登录，如果失效了那么就重新登录
        # request.GET 是个class,里面包含有cookie相关的字典
        request.session = SessionStore(request.GET['code'])
        # modify session lifetime, so make user's cookie can stay longger in db
        # 根据sessionid找到存储的对应的session，然后更改其生成时间戳，这样cookie相当于延长了生命周期
        request.session.modified = True
        return redirect(index)
    else:
        print "not auth"
        return redirect_to_login(
            request.build_absolute_uri(),
            settings.SSO_AUTH_URL, 'callback')
