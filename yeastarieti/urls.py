from django.urls import path
from . import views
from . import api
from .views import LoginView

urlpatterns = [
    path("", views.home, name ="home"),
    path('logout', views.logout_view, name='logout'),
    path('sendsms', views.sendsms, name='sendsms'),
    path('api/login/',api.login),
    path('api/logout',api.logout),
    path('dashboard/',views.dashboard, name ="dashboard"),
]
