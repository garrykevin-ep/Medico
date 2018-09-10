from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^diaflow/',views.diaflow),
    url(r'^stock/', views.stock_list)
]
