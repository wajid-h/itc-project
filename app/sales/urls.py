from django.urls import path
from . import views
urlpatterns = [
    path('' , views.index , name= 'index' ) , 
    path('onboard',  views.onboard , name = 'login'),
    path('logout', views.front_logout , name='logout')
] 