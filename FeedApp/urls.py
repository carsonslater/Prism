from django.urls import path
from . import views

# app_name helps Django distinguish this app's URLs from others.
# This allows us to use 'FeedApp:index' in our templates and views.
app_name = 'FeedApp'

# urlpatterns defines the list of valid URLs for this app.
# path() arguments:
# 1. The URL pattern string ('' matches the root URL of this app).
# 2. The view function to call when this pattern is matched.
# 3. The name argument allows us to refer to this URL pattern elsewhere in the code.
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('myfeed/', views.myfeed, name='myfeed'),
    path('new_post/', views.new_post, name='new_post'),
    # <int:post_id> is a path converter. It captures an integer from the URL 
    # and passes it as the 'post_id' argument to the comments view function.
    path('comments/<int:post_id>/', views.comments, name='comments'),
    path('friends/', views.friends, name='friends'),
    path('friendsfeed/', views.friendsfeed, name='friendsfeed'),
]
