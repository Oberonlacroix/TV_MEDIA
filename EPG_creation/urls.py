from django.urls import path
from .views import EPG, logout_view
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('EPG_creation', EPG.as_view(), name='epg_generator'),
    path('logout/', logout_view, name='logout'),
]
