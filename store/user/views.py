from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from .models import UserInfo
from goods.models import GoodsInfo
from hashlib import sha1
from order.models import OrderInfo
from . import user_decorator
from django.core.paginator import Paginator,Page
import sys
# Create your views here.
sys.path.append('/home/lxhsec/lxhsec/django/store/goods')
sys.path.append('/home/lxhsec/lxhsec/django/store/order')
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse

def register(request):
    return render(request, 'user/register.html')

def login(request):
    return render(request, 'user/login.html')

def register_exist(request):
    uname=request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    if(ucpwd != upwd):
        return redirect('/user/register')
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    spwdSha1 = s1.hexdigest()
    new_user = UserInfo()
    new_user.uname = uname
    new_user.upwd = spwdSha1
    new_user.uemail = uemail
    new_user.save()
    return redirect('/user/login')

def loginhandle(request):
    post = request.POST
    verify = post.get('verify')
    verify = verify.upper()
    # 2.获取浏览器请求当中的session中的值
    verifycode = request.session.get('verifycode')
    # 3.判断两个验证码是否相同
    if verify != verifycode:
        return HttpResponse('验证码错误')
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu','0')
    name = UserInfo.objects.filter(uname=uname)  #[]查出来的是一个列表
    if(len(name)) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        spwdSha1 = s1.hexdigest()
        # print(spwdSha1)
        if(spwdSha1 == name[0].upwd):
            url = request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)
            red.set_cookie('url','',max_age=-1)
            if(jizhu)!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['id'] = name[0].id
            request.session['uname'] = name[0].uname
            return red
        else:
            context= {'error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'user/login.html',context)
    else:
        context={'error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'user/login.html',context)
    # else:
    #     # context={'error_code':1}
    #     # return render(request,'user/login.html',context)
    #     

def logout(request):
    request.session.flush()
    return redirect('/')

@user_decorator.login
def user_center_info(request):
    email = UserInfo.objects.get(id = request.session['id']).uemail
    goods_list = []
    goods_ids =request.COOKIES.get('goods_ids','')
    if goods_ids != '':
        goodlist = goods_ids.split(',')
        for each in goodlist:
            goods_list.append(GoodsInfo.objects.get(id=int(each)))
    context = {'info': '用户中心','active':'info','user_center':1,
               'goods_list':goods_list, 'email': email, 'uname': request.session['uname']}
    return render(request, 'user/user_center_info.html',context)

@user_decorator.login
def user_center_order(request,pindex):
    order = OrderInfo.objects.filter(user_id=request.session['id'])
    paginator=Paginator(order,2)
    if pindex=='':
        pindex='1'
    page=paginator.page(int(pindex))
    context = {'info': '用户中心','active':'order','user_center':1,
               'order': order,'page': page, 'paginator': paginator}
    return render(request, 'user/user_center_order.html',context)

@user_decorator.login
def user_center_site(request):
    user = UserInfo.objects.get(pk=request.session['id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('receive')
        user.uaddress = post.get('addr')
        user.uyoubian = post.get('postcode')
        user.uphone = post.get('phone')
        user.save()
    context = {'info': '用户中心','active':'site','user':user,'user_center':1}
    return render(request, 'user/user_center_site.html',context)

def verify_code(request):
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

#
# # def verify_check2(request):
#     """验证码的验证"""
#     # 1.获取post请求当中的输入验证码的内容
#     verify = request.POST.get('verify')
#     # 2.获取浏览器请求当中的session中的值
#     verifycode = request.session.get('verifycode')
#     # 3.判断两个验证码是否相同
#     if verify == verifycode:
#         return HttpResponse('ok')
#     else:
#         return HttpResponse('err')


# def show_verify2(request):
#     """显示验证码界面"""
#     return render(request, 'booktest/show_verify2.html')