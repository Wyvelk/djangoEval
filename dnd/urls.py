from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.authView, name="authView"),
]