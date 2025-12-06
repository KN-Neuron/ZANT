from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Dodaj tę linię poniżej:
    path('api/analyze/', views.analyze_accident, name='analyze_accident'),
]