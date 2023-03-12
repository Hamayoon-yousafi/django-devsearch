from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_page, name='login'),
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_profile, name='user-profile'),
]