from django.urls import path
from . import views

urlpatterns = [
    path('upload/',  views.upload_resume,  name='upload_resume'),
    path('matches/', views.resume_matches, name='resume_matches'),
]