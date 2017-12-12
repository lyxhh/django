from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^register$',views.register),
    url(r'^register_handle',views.register_handle),
    url(r'^register_exist/$',views.register_exist),
    url(r'^login$',views.login),
    url(r'^loginhandle/$',views.loginhandle),
    url(r'^user_center_info/$',views.user_center_info),
    url(r'^user_center_order(\d*)/$',views.user_center_order),
    url(r'^user_center_site/$',views.user_center_site),
    url(r'^logout/$',views.logout),
    url(r'^verify_code/$', views.verify_code),
]
