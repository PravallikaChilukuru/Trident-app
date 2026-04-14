from django.conf.urls import url
from .views import vm_health

urlpatterns = [
    url(r'^health/$', vm_health),
]
