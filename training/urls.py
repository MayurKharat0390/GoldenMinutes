from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('', views.training_list, name='list'),
    path('<slug:slug>/', views.training_detail, name='detail'),
    path('<slug:slug>/submit/', views.submit_quiz, name='submit_quiz'),
]
