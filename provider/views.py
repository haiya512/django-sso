# coding: utf-8
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.views import redirect_to_login
from django.conf import settings
from api import my_render, require_login
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect, HttpResponse
from forms import LoginForm


def index(request):
    if request.user.is_authenticated():
        # 这里的作用是: 从client那边跳过来要登录,登录之后, 在这里做判断之后再跳回 client
        #
        # settings.SESSION_COOKIE_NAME default value is 'sessionid'
        # print "user is already logined, now redirect to destination urls"
        print "这里会进行第二步"
        try:
            callback = request.GET['service']
            cookie = request.COOKIES[settings.SESSION_COOKIE_NAME]
            return redirect(callback + '?code=' + cookie)
        except:
            return HttpResponse("Hello world")

    else:
        # request.get_full_path() is /?callback=http://127.0.0.1:8000/
        # reverse('admin:login') value is /admin/login/
        # url just like this: http://127.0.0.1:9000/admin/login/?next=/%3Fcallback%3Dhttp%253A//127.0.0.1%253A8000/
        # redirect_field_name is callback
        # login_url is http://127.0.0.1:7000/
        # settings.LOGIN_URL is /accounts/login/
        # resolved_url is : http://127.0.0.1:7000/
        print "get_full path is %s" % request.get_full_path()
        print "没有登录,第一步"
        return redirect_to_login(
            request.get_full_path(), reverse('admin:login'))


def login(request):
    # 如果检测到session中有username, 并且有callback 字符串
    # 检查callback 是否是个有效的地址,如果无效,则置空,去掉这个字符串,进行下一步
    # 检测username是否对, 如果不对重新登录,对的话重定向到上面的地址
    app_path = request.get_full_path()

    # 如果用户已登录
    # if request.user.is_authenticated():
    #     sessionid = request.COOKIES[settings.SESSION_COOKIE_NAME]
    #     # return redirect(callback + '?code=' + sessionid)
    #     # return HttpResponseRedirect('/')
    #     # try:
    #     #     # callback = request.GET['callback']
    #     #     # print "callback is : %s" % callback
    #     #     # for key, value in request.GET:
    #     #     #     print "%s: %s" % (key, value)
    #     #     # print request.GET('callback', '')
    #     #     # print request.GET['next']
    #     #     print request.GET['callback']
    #     # except:
    #     #     callback = None
    #     #     print "callback is none"
    #     if request.method == 'GET' and 'next' in request.GET:
    #         _next = request.GET['next']
    #         print _next
    #     else:
    #         _next = '/'
    #     return redirect(_next)
    # 如果用户未登录

    if request.method == "POST":
        uf = LoginForm(request, data=request.POST)
        if uf.is_valid():
            auth.login(request, uf.get_user())
            username = uf.cleaned_data['username']
            request.session['username'] = username
            print "next is : %s" % request.GET['next']
            return redirect(request.GET['next'])
    else:
        form = LoginForm(request)

    return my_render('cas/login.html', locals(), request)


@require_login
def new_index(request):
    username = request.session.get('username')
    try:
        callback = request.GET['callback']
        cookie = request.COOKIES[settings.SESSION_COOKIE_NAME]
        return redirect(callback + '?code=' + cookie)
    except:
        return HttpResponse("Hello <strong>%s</strong>, this is sso server welcome page" % username)
    # return render_to_response('index.html', {'username': username})


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


def register(request):
    pass
