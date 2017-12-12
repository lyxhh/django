from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',views.cart),
    url(r'^add_(\d+)_(\d+)/$',views.addcart),
    url(r'^delete_(\d+)/$',views.delete),
    url(r'^edit_(\d+)_(\d+)/$',views.edit),

]