"""FeedProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


# urlpatterns is a list where we define the mapping between URLs and the views that handle them.
urlpatterns = [
    # 'admin/' routes to the built-in Django administration site.
    path('admin/', admin.site.urls),
    # include('FeedApp.urls') tells Django to look into FeedApp/urls.py for any URLs starting with root '' (empty string).
    # This keeps our URL configuration modular.
    path('', include('FeedApp.urls')),
    # include('users.urls') routes any URL not matched above to the users app IF it matches patterns in users/urls.py. 
    # (Note: path() matching checks patterns in order).
    path('users/', include('users.urls')),
]

# If we are in DEBUG mode (local development), we might want to serve static/media files differently.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
