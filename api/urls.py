from django.conf.urls import url

from api.views import data, index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^data$', data, name='data'),
]
