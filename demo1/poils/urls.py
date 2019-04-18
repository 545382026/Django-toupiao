from django.conf.urls import url
from . import views
app_name = 'poils'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^choice/(\d+)/$', views.choice, name='choice'),
    url(r'^choicehand/$', views.choicehand, name='choicehand'),
    url(r'^result/$', views.result, name='result')
]