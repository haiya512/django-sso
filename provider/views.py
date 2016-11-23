# coding: utf-8
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import redirect_to_login
from django.conf import settings


def index(request):
    if request.user.is_authenticated():
        # 这个貌似作用不大，基本上不会跳转到这里，在consumer那里已经做了判断
        # settings.SESSION_COOKIE_NAME default value is 'sessionid'
        # request.get_full_path() is /?callback=http://127.0.0.1:8000/
        return redirect(request.GET['callback'] +
            '?code=' + request.COOKIES[settings.SESSION_COOKIE_NAME])
    else:
        # reverse('admin:login') value is /admin/login/
        # url just like this: http://127.0.0.1:9000/admin/login/?next=/%3Fcallback%3Dhttp%253A//127.0.0.1%253A8000/
        return redirect_to_login(
            request.get_full_path(), reverse('admin:login'))

