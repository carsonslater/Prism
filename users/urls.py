from django.urls import path, include

from . import views


app_name = 'users'

urlpatterns = [
    # Include default auth urls.
    # This includes built-in patterns for login, logout, password change, etc.
    # Django provides these views automatically.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
    ]