from django.urls import path
from . import views

from django.urls import path
from .views import *
urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('search/', views.searchList, name='search'),
    path('exportcsv/', views.exportcsv, name='exportcsv'),
    path('detail_image/<int:id>', views.view_image_binary, name='detail_image'),
]