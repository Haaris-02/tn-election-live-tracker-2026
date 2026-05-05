from django.urls import path
from . import views

urlpatterns = [
    path('api/constituencies/', views.get_constituencies, name='get_constituencies'),
]