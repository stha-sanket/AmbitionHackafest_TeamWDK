from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('add/', views.medicine_add, name='medicine_add'),
    path('<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
    path('<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),
    path('pos/', views.pos_view, name='pos_view'),
]