from django.urls import path 
from .views import SignUpView,LoginView,LogoutView,HomeView

urlpatterns = [
    path('signup/',SignUpView.as_view(),name = 'signup'),
    path('login/',LoginView.as_view(),name = 'login'),
    path('logout/',LogoutView.as_view(), name = 'logout'),
    path('',HomeView.as_view(),name = 'home'),
]
