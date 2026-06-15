from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Post, Category


def index(request):
    """Главная страница: 5 последних опубликованных постов."""
    post_list = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).select_related(
        'category', 'location', 'author'
    ).order_by('-pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    """Страница отдельной публикации."""
    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        pk=pk,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Страница категории с постами."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.post_set.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    ).select_related(
        'location', 'author'
    ).order_by('-pub_date')
    context = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)
