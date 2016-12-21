from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/search/$', views.SearchView.as_view(), name='SearchView'),
    url(r'^', views.IndexView.as_view())
]
