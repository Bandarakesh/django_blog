from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),  # This is the correct path for registration
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),
    path('create_post/', views.create_post, name='create_post'),
]
