from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/new/', views.event_create, name='event_create'),
    path('event/<int:pk>/register/', views.event_register, name='event_register'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('manage-registrations/', views.manage_registrations, name='manage_registrations'),
    path('approve-registration/<int:pk>/', views.approve_registration, name='approve_registration'),
    path('dashboard/', views.dashboard, name='dashboard'),
] 