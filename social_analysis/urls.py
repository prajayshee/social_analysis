"""
URL configuration for social_analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app.views import get_avg_engagement, get_posts_by_type, list_all_posts, avg_engagement,posts_by_type

urlpatterns = [
    path('admin/', admin.site.urls),
    path('avg-engagement/', get_avg_engagement, name='avg_engagement'),
    path('posts/<str:post_type>/', get_posts_by_type, name='get_posts_by_type'),
    path('list-posts/', list_all_posts, name='list_all_posts'),
    path('avg-engagement/', avg_engagement, name='avg_engagement'),
    path('posts/<str:post_type>/', posts_by_type, name='get_posts_by_type'),
]
