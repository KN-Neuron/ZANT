from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/analyze/', views.analyze_accident, name='analyze_accident'),
    path('api/generate-pdf/', views.generate_pdf, name='generate_pdf'),
]