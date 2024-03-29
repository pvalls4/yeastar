from django.urls import path
from . import views
from . import api

urlpatterns = [
    path("", views.dashboard, name ="dashboard"),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('token/', views.token, name='token'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('delete_contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('contacts/', views.contacts, name='contacts'),
    path('message_success/', views.message_success, name='message_success'),
    path('createuser/', views.create_user, name='create_user'),
    path('api/login/',api.login),
    path('api/logout/',api.logout),
    path('api/sendsms/', views.api_sendsms, name='api_sendsms'),
]
