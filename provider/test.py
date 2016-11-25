# coding: utf8
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, RequestContext
from django.template import RequestContext
from models import User
from api import require_login


def login(req):
    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = User.objects.filter(username=username, password=password)
        if user:
            req.session['username'] = username
            if req.session['username'] == '':
                return HttpResponseRedirect('/accounts/login/')
            else:
                return HttpResponseRedirect('/index/')
        else:
            print "user is kong"
            if User.objects.filter(username=username):
                return HttpResponseRedirect('/accounts/login/')
            else:
                return HttpResponseRedirect('/register/')
    else:
        return render_to_response('login.html', context_instance=RequestContext(req))

@require_login
def index(request):
    username = request.session.get('username')
    return render_to_response('index.html', {'username': username})


@require_login
def logout(request):
    session = request.session.get('username', False)
    if session:
        del request.session['username']
        print "del session"
        return HttpResponseRedirect('/accounts/login/')
    else:
        print "not del session"
        return HttpResponseRedirect('/accounts/login/')
