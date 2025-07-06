from django.urls import path
from . import views

urlpatterns = [
    path('', views.bloodunit_list, name='bloodunit_list'),
    path('add/', views.bloodunit_add, name='bloodunit_add'),
    path('<int:pk>/', views.bloodunit_detail, name='bloodunit_detail'),
    path('<int:pk>/edit/', views.bloodunit_edit, name='bloodunit_edit'),
    path('<int:pk>/delete/', views.bloodunit_delete, name='bloodunit_delete'),
    path('pos/', views.bloodunit_list, name='bloodunit_pos'),
]