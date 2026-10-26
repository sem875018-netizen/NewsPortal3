from django.urls import path

from . import views
from .models import Post


urlpatterns = [
    # Новости
    path("news/", views.news_list, name="news_list"),
    path("news/search/", views.news_search, name="news_search"),
    path(
        "news/create/",
        views.PostCreateView.as_view(),
        {"post_type": Post.NEWS},
        name="news_create",
    ),
    path(
        "news/<int:pk>/edit/",
        views.PostUpdateView.as_view(),
        {"post_type": Post.NEWS},
        name="news_edit",
    ),
    path(
        "news/<int:pk>/delete/",
        views.post_delete,
        {"post_type": Post.NEWS},
        name="news_delete",
    ),
    path("news/<int:pk>/", views.news_detail, name="news_detail"),

    # Статьи
    path(
        "articles/create/",
        views.PostCreateView.as_view(),
        {"post_type": Post.ARTICLE},
        name="article_create",
    ),
    path(
        "articles/<int:pk>/edit/",
        views.PostUpdateView.as_view(),
        {"post_type": Post.ARTICLE},
        name="article_edit",
    ),
    path(
        "articles/<int:pk>/delete/",
        views.post_delete,
        {"post_type": Post.ARTICLE},
        name="article_delete",
    ),
]