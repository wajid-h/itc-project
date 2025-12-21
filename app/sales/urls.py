from django.urls import path
from . import views
urlpatterns = [

    path('', views.index, name='index'),
    path('report/<int:id>' , views.sales_report , name= 'sales-report' ) , 
    path('sales/<int:id>' , views.index_business , name= 'index-business' ) , 
    path('onboard',  views.onboard , name = 'login'),
    path('logout', views.front_logout , name='logout'),
] 