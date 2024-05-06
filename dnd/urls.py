from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.authView, name="authView"),
    path("dice/", views.dice, name="dice"),
    path('roll_dice/', views.roll_dice, name='roll_dice'),
    path('ranking/', views.ranking, name='ranking'),
    path('logout/', views.Logout, name='custom_logout'),
    path('startAdventure/', views.startAdventure, name='startAdventure'),
    path('adventure/', views.adventure, name='adventure'),
    path('endAdventure/', views.endAdventure, name='endAdventure'),
    path('rules/', views.rules, name='rules')
]