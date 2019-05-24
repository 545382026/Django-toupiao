from django.conf.urls import url
from . import views
app_name = 'poils'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^loginout/$', views.loginout, name='loginout'),
    url(r'^register/$', views.register, name='register'),

    url(r'^choice/(\d+)/$', views.choice, name='choice'),
    url(r'^choicehand/$', views.choicehand, name='choicehand'),
    url(r'^result/$', views.result, name='result'),

    # 登录认证
    url(r'^authen/(.*?)/$', views.authen, name='authen'),
    # 验证码
    url(r'^verify/$', views.verify, name='verify'),
    # ajax异步刷新
    url(r"^checkuser/$", views.checkuser, name='checkuser'),

]