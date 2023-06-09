from django.urls import path
from . import views
from . import api
from .views import LoginView

urlpatterns = [
    path("", views.home, name ="home"),
    path('api/login/',api.login),
    path('dashboard/',views.dashboard, name ="dashboard"),
]
