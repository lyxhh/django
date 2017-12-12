from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import CartInfo
from user import user_decorator
import sys
sys.path.append('/home/lxhsec/lxhsec/django/store/user')
# Create your views here.

@user_decorator.login
def cart(request):
    userid = request.session['id']
    cartlist = CartInfo.objects.filter(user_id = userid)
    context = {'info': '购物车', 'user_center': 0, 'cartlist': cartlist}
    return render(request, 'cart/cart.html', context)

@user_decorator.login
def addcart(request, gid, count1):
    userid = request.session['id']
    gid = int(gid)
    count1 = int(count1)
    carts = CartInfo.objects.filter(user_id=int(userid),goods_id=gid) # []
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count1
    else:
        cart = CartInfo()
        cart.count = 1
        cart.user_id = userid
        cart.goods_id = gid
    cart.save()
    if request.is_ajax():
        num = CartInfo.objects.filter(user_id=int(userid)).count()
        return JsonResponse({'cart_id':cart.id,'count':num})
    else:
        return redirect('/cart')

@user_decorator.login
def delete(request,cart_id):
    cart = CartInfo.objects.get(pk = int(cart_id))
    cart.delete()
    return redirect('/cart')

@user_decorator.login
def edit(request, cart_id, count):
    count1 = 1
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.count = int(count)
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count1}
    return JsonResponse(data)
