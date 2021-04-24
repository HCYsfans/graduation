from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/$', views.home, name="home"),
    url(r'^handle/(\d+)/$', views.handle, name="handle"),
    url(r'^exhibit/(\d+)/$', views.exhibit, name="exhibit"),
    url(r'^mine/(\d+)/$', views.mine, name="mine"),
    url(r'^sc/$',views.sc,name="sc"),
    url(r'^sctp/(\d+)/$',views.sctp,name="sctp"),
    url(r'^check/(\d+)/$',views.check,name="check"),
    url(r'^manipulate/(\d+)/$',views.manipulate,name="manipulate"),
    url(r'^login/$',views.login,name="login"),
    url(r'^register/$',views.register,name="register"),
    url(r'^quit/$',views.quit,name="quit"),
    url(r'^checkuserid/$',views.checkuserid,name="checkuserid"),
    url(r'^checkuserpsd/$',views.checkuserpsd,name="checkuserpsd"),
    url(r'^modify/$',views.modify,name="modify"),
    url(r'^security/$',views.security,name="security"),
]