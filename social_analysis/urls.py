from django.contrib import admin
from django.urls import path
from app.views import get_avg_engagement, get_posts_by_type, list_all_posts, base,search_posts_by_type

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base, name='base'),
    path('avg-engagement/', get_avg_engagement, name='avg_engagement'),
    path('posts/<str:post_type>/', get_posts_by_type, name='get_posts_by_type'),
    path('posts/', get_posts_by_type, name='get_posts_by_type_no_type'),
    path('list-posts/', list_all_posts, name='list_all_posts'),
    path('search_posts/', search_posts_by_type, name='search_posts_by_type'), 
]
