from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('add/', views.patient_add, name='patient_add'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('reports/', views.diagnosis_report_list, name='diagnosis_report_list'),
] 