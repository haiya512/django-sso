# coding: utf-8
from django.shortcuts import render_to_response
# from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.views import redirect_to_login


def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))


def require_login(func):
    """
    要求登录的装饰器
    """
    def _deco(request, *args, **kwargs):
        if not request.session.get('username'):
            return redirect_to_login(request.get_full_path(), reverse('loginurl'))
            # return HttpResponseRedirect(reverse('loginurl'))
        return func(request, *args, **kwargs)
    return _deco
