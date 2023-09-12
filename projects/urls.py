from django.urls import path
from projects import views

urlpatterns = [
    path('projects/', views.ProfileList.as_view()),
    path('projects/<int:pk>/', views.ProfileDetail.as_view()),
]
