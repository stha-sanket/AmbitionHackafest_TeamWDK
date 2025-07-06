from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('add/', views.doctor_add, name='doctor_add'),
    path('<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('<int:pk>/edit/', views.doctor_edit, name='doctor_edit'),
    path('<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
] 