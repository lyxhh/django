from django.shortcuts import render
from .models import GoodsInfo,TypeInfo
from django.core.paginator import Paginator,Page
from cart.models import CartInfo
import sys
sys.path.append('/home/lxhsec/lxhsec/django/store/cart')
# Create your views here.
def index(request):
    # 最新最火
    type = TypeInfo.objects.all() # [返回一个列表]
    haixian = type[0].goodsinfo_set.order_by('-id')[0:4]
    haixian1 = type[0].goodsinfo_set.order_by('-gclick')[0:4]

    fruit = type[1].goodsinfo_set.order_by('-id')[0:4]
    fruit1 = type[1].goodsinfo_set.order_by('-gclick')[0:4]

    sudong = type[2].goodsinfo_set.order_by('-id')[0:4]
    sudong1 = type[2].goodsinfo_set.order_by('-gclick')[0:4]

    meet = type[3].goodsinfo_set.order_by('-id')[0:4]
    meet1 = type[3].goodsinfo_set.order_by('-gclick')[0:4]

    egg = type[4].goodsinfo_set.order_by('-id')[0:4]
    egg1 = type[4].goodsinfo_set.order_by('-gclick')[0:4]

    avag = type[5].goodsinfo_set.order_by('-id')[0:4]
    avag1 = type[5].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'haixian': haixian, 'haixian1': haixian1, 'fruit': fruit,
               'fruit1': fruit1, 'sudong': sudong,
               'sudong1': sudong1, 'meet': meet, 'meet1': meet1,
               'egg': egg, 'egg1': egg1, 'avag': avag, 'avag1': avag1,
               'goods': 'index'}
    return render(request, 'goods/index.html',context)

def list(request, tid, sort, pindex):
    type = TypeInfo.objects.get(pk=int(tid))
    new = type.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator=Paginator(goods_list,5)
    page=paginator.page(int(pindex))
    context = {'new': new, 'page': page, 'pindex': pindex,
               'sort': sort, 'typeinfo':type, 'paginator': paginator}
    return render(request,'goods/list.html',context)

def detail(request, id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick += 1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'goods': goods, 'news': news}
    response = render(request,'goods/detail.html',context)

    goods_ids = request.COOKIES.get('goods_ids','')
    goodsid = '%d' % goods.id
    if goods_ids != '':
        gids_list = goods_ids.split(',')
        if gids_list.count(goodsid) >=1:
            gids_list.remove(goodsid)
        gids_list.insert(0,goodsid)

        if len(gids_list)>=6:
            del gids_list[5]
        goods_ids = ','.join(gids_list)
    else:
        goods_ids = goodsid
    response.set_cookie('goods_ids',goods_ids)

    return response

# 购物车数量
def cart_count(request):
    if request.session.__contains__('id'):
        # print('存在id')
        return CartInfo.objects.filter(user=request.session['id']).count()
    else:
        return 0

from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title']= '搜索'
        context['guest_cart']=1
        context['cart_count']=cart_count(self.request)
        # print(cart_count(self.request))
        return context