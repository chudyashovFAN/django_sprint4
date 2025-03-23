from django.urls import path
from django.contrib.auth import get_user_model

from . import views


app_name = 'blog'

User = get_user_model()

urlpatterns = [
    path('', views.PostList.as_view(), name='index'),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(), name='post_detail'
    ),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        'posts/<int:post_id>/comment/',
        views.PostComment.as_view(), name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.CommentUpdate.as_view(), name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.CommentDelete.as_view(), name='delete_comment'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.PostUpdateView.as_view(), name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.PostDeleteView.as_view(), name='delete_post'
    ),
    path(
        'profile/edit/',
        views.ProfileUpdateView.as_view(), name='edit_profile'
    ),
    path(
        'profile/<slug:username>/',
        views.profile_view, name='profile'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts, name='category_posts'
    )
]
