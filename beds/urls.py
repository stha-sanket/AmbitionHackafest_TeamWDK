from django.urls import path
from . import views

urlpatterns = [
    path('', views.bed_list, name='bed_list'),
    path('add/', views.bed_add, name='bed_add'),
    path('<int:pk>/', views.bed_detail, name='bed_detail'),
    path('<int:pk>/edit/', views.bed_edit, name='bed_edit'),
    path('<int:pk>/delete/', views.bed_delete, name='bed_delete'),
    path('waiting-list/', views.waiting_list, name='waiting_list'),
    path('waiting-list/add/', views.waiting_add, name='waiting_add'),
    path('waiting-list/<int:pk>/delete/', views.waiting_delete, name='waiting_delete'),
    path('icu/', views.icu_list, name='icu_list'),
] 