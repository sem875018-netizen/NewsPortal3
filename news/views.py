from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, UpdateView

from .filters import PostFilter
from .forms import PostForm
from .models import Post


def home(request):
    return HttpResponse("Добро пожаловать на сайт новостей!")


def news_list(request):
    posts = Post.objects.filter(post_type=Post.NEWS).order_by("-created_at")
    page_obj = Paginator(posts, 10).get_page(request.GET.get("page"))

    return render(
        request,
        "news/news_list.html",
        {"posts": page_obj.object_list, "page_obj": page_obj},
    )


def news_search(request):
    posts = Post.objects.filter(post_type=Post.NEWS).order_by("-created_at")
    post_filter = PostFilter(request.GET, queryset=posts)
    page_obj = Paginator(post_filter.qs, 10).get_page(request.GET.get("page"))

    return render(
        request,
        "news/news_search.html",
        {
            "filter": post_filter,
            "posts": page_obj.object_list,
            "page_obj": page_obj,
        },
    )


def news_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, post_type=Post.NEWS)
    return render(request, "news/news_detail.html", {"post": post})


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "news/post_form.html"
    permission_required = "news.add_post"

    def form_valid(self, form):
        form.instance.post_type = self.kwargs["post_type"]
        return super().form_valid(form)

    def get_success_url(self):
        if hasattr(self.object, "get_absolute_url"):
            return self.object.get_absolute_url()
        return "/"


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "news/post_form.html"
    permission_required = "news.change_post"

    def get_queryset(self):
        queryset = super().get_queryset()
        post_type = self.kwargs.get("post_type")

        if post_type is not None:
            queryset = queryset.filter(post_type=post_type)

        return queryset

    def get_success_url(self):
        if hasattr(self.object, "get_absolute_url"):
            return self.object.get_absolute_url()
        return "/"


def post_delete(request, pk, post_type):
    post = get_object_or_404(Post, pk=pk, post_type=post_type)

    if request.method == "POST":
        post.delete()
        return redirect("/")

    return render(request, "news/post_confirm_delete.html", {"post": post})