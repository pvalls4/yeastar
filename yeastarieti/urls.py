from django.urls import path
from . import views
from . import api
from .views import LoginView

urlpatterns = [
    path("", views.home, name ="home"),
    path('logout', views.logout_view, name='logout'),
    path('sendsms', views.sendsms, name='sendsms'),
    path('message_success/', views.message_success, name='message_success'),
    path('api/login/',api.login),
    path('api/logout',api.logout),
    path('api/sendsms', views.api_sendsms, name='api_sendsms'),
    path('dashboard/',views.dashboard, name ="dashboard"),
]
