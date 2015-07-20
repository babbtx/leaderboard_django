from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<company_uid>[^/]+)/$', views.company, name='by_company'),
]
