# url.py file for a single django app

from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/register/', views.CogsciNetworkRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'memberlist', views.MemberList.as_view(), name='memberlist'),
    path(r'settings', views.SettingsView.as_view(), name='settings'),
    path(r'profile/<int:pk>', views.ProfileDetailsView.as_view(), name='profile_show'),
    path(r'profile/<int:pk>/update', views.ProfileUpdateView.as_view(), name='profile_update'),
    path(r'profile/<int:pk>/delete', views.ProfileDeleteView.as_view(), name='profile_delete'),
    path(r'join', views.ProfileUpdateView.as_view(), name='join'),
    path(r'', views.HomeView.as_view(), name='home'),
    # path(r'about/', views.about, name='about'),
]
