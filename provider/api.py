# coding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))


def require_login(func):
    """
    要求登录的装饰器
    """
    def _deco(request, *args, **kwargs):
        if not request.session.get('username'):
            return HttpResponseRedirect('/login/')
        return func(request, *args, **kwargs)
    return _deco
