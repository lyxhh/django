from django.http import HttpResponseRedirect
from django.shortcuts import redirect

def login(func):
    def login_fun(reqeust, *args, **kwargs):
        if(reqeust.session.__contains__('uname')):
            return func(reqeust,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login')
            red.set_cookie('url',reqeust.get_full_path())
            return red
    return login_fun