from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Tag, News
# from .forms import NewNewsForm
from comment.models import Comment
from comment.forms import CommentForm

# Create your views here.


def news_list(request):
    news = News.objects.all().order_by('-date_posted')
    paginator = Paginator(news, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'news_list.html', context)


def news_details(request, news_id):
    news = get_object_or_404(News, id=news_id)
    user = request.user

    # comment
    comments = Comment.objects.filter(news=news).order_by('date')

    # Comments Form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('news_details', args=[news_id]))
    else:
        form = CommentForm()

    comments_counts = Comment.objects.filter(news=news).count()

    context = {
        'news': news,
        'form': form,
        'comments': comments,
        'comments_counts': comments_counts
    }

    return render(request, 'news_detail.html', context)

#
# @login_required
# def new_news(request):
#     user = request.user
#     tags_objs = []
#
#     if request.method == 'POST':
#         form = NewNewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             picture = form.cleaned_data.get('picture')
#             title = form.cleaned_data.get('title')
#             tags_form = form.cleaned_data.get('tags')
#             details = form.cleaned_data.get('details')
#
#             tags_list = list(tags_form.split(','))
#
#             for tag in tags_list:
#                 t, created = Tag.objects.get_or_create(title=tag)
#
#             p = News.objects.create(picture=picture, title=title, details=details, author=user)
#             p.tags.set(tags_objs)
#             p.save()
#             return redirect('index')
#     else:
#         form = NewNewsForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'newnews.html', context)


def news_tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    news = News.objects.filter(tags=tag).order_by('-date_posted')

    paginator = Paginator(news, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'tag': tag,
    }

    return render(request, 'tag_news_view.html', context)