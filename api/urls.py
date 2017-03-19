from django.conf.urls import url

from api.views import index

urlpatterns = [
    url(r'^$', index, name='index'),
]
