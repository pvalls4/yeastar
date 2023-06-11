from django.urls import path
from . import views
from . import api
from django.contrib.auth import views as auth_views
#from .views import LoginView

urlpatterns = [
    path("", views.dashboard, name ="dashboard"),
    path('logout', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('sendsms', views.sendsms, name='sendsms'),
    path('message_success/', views.message_success, name='message_success'),
    path('createuser/', views.create_user, name='create_user'),
    path('api/login/',api.login),
    path('api/logout',api.logout),
    path('api/sendsms', views.api_sendsms, name='api_sendsms'),
]
