from django.urls import path
from . import views

urlpatterns = [
    path('', views.admission_list, name='admission_list'),
    path('add/', views.admission_add, name='admission_add'),
    path('<int:pk>/', views.admission_detail, name='admission_detail'),
    path('<int:pk>/edit/', views.admission_edit, name='admission_edit'),
    path('<int:pk>/discharge/', views.admission_discharge, name='admission_discharge'),
    path('<int:pk>/delete/', views.admission_delete, name='admission_delete'),
    path('visits/', views.hospital_visits, name='hospital_visits'),
] 