from django.shortcuts import render,redirect
from user.models import UserInfo
from cart.models import CartInfo
from .models import OrderDetailInfo, OrderInfo
from user import user_decorator
from datetime import datetime
from django.db import transaction
import sys
sys.path.append('/home/lxhsec/lxhsec/django/store/cart')
sys.path.append('/home/lxhsec/lxhsec/django/store/user')
# Create your views here.
def order(reqeust):
    user_id = reqeust.session['id']
    user = UserInfo.objects.get(id=int(user_id))
    get = reqeust.GET
    cartlist = get.getlist('cart_id')
    cartid = [int(each) for each in cartlist]
    carts = CartInfo.objects.filter(id__in=cartid)

    context = {'info': '提交订单','user_center': 0, 'carts': carts, 'user': user,'cart_ids':','.join(cartlist)}
    return render(reqeust, 'order/place_order.html',context)
'''
事务：一旦操作失败则全部回退
1、创建订单对象
2、判断商品的库存
3、创建详单对象
4、修改商品库存
5、删除购物车

oid = models.CharField(max_length=20, primary_key=True)
user = models.ForeignKey('user.UserInfo')
odate = models.DateTimeField(auto_now_add=True)
oIsPay = models.BooleanField(default=False)
ototal = models.DecimalField(max_digits=6, decimal_places=2)
oaddres = 地址



class OrderDetailInfo(models.Model):
    goods=models.ForeignKey('goods.GoodsInfo')
    order=models.ForeignKey(OrderInfo)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    count=models.IntegerField()
'''

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    post = request.POST
    addres = post.get('address')
    cart_ids = post.get('cart_ids')
    cartlist = [int(items) for items in cart_ids.split(',')]
    user_id = request.session['id']
    try:
        order = OrderInfo()
        order.oid = '%s%d' % (datetime.now().strftime('%Y%m%d%H%M%S'),user_id)
        order.user_id = user_id
        order.ototal = 0
        order.oaddress = addres
        order.save()
        total = 0
        for each in cartlist:
            detail = OrderDetailInfo()
            detail.order = order
            cartid = CartInfo.objects.get(id=each)
            print(cartid)
            goods = cartid.goods
            if goods.gkucun >= cartid.count:
                goods.gkucun = cartid.goods.gkucun - cartid.count
                goods.save()
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cartid.count
                detail.save()
                total = total + goods.gprice * cartid.count
                cartid.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart')
        order.ototal = total + 10
        order.save()
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print(e)
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/user_center_order/')

@user_decorator.login
def pay(request,oid):
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = True
    order.save()
    context = {'order': order}
    return render(request,'order/pay.html',context)
