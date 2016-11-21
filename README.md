# django-sso
Simple SSO implementation in Django

只有一个登陆的按钮,很简单。登出的功能没做, 记录登陆操作的功能也没做
有一个不好的地方是: provider本身登陆的时候会报错

## How to start

    $ python consumer.py migrate
    $ python provider.py migrate
    $ python provider.py createsuperuser
    $ python consumer.py runserver 127.0.0.1:8000 & python provider.py runserver 127.0.0.1:9000
