import json
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from webprofile.forms import PostForms
from webprofile.models import Post
from profiles.models import Profile

import views_validations


def index(request):
    # All posts of all users
    posts = views_validations.separate_posts_into_quantity_groups(
        posts_list=(
            Post.objects.order_by(  # type: ignore
                '-publication_date').filter(is_published=True)),
        items_quantity=2)

    # Posts per page
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts_per_page = paginator.get_page(page)

    # Context
    context = {
        'url_context': 'index',
        'posts_per_page': posts_per_page}

    # Add Profile to context
    if request.user.is_authenticated:
        try:
            user_profile = get_object_or_404(Profile, user=request.user.id)
        except Exception as err:
            print(err)
            user_profile = None

        context['user_profile'] = user_profile

    return render(request, 'index.html', context)


def search_post(request):
    posts = []
    if 'q' in request.GET:
        posts = Post.objects.order_by(  # type: ignore
            '-publication_date').filter(is_published=True).filter(
            title__icontains=request.GET['q'])

    # Card groups
    posts = views_validations.separate_posts_into_quantity_groups(
        posts_list=posts, items_quantity=2)

    # Posts per page
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts_per_page = paginator.get_page(page)

    # Context
    context = {
        'url_context': 'index',
        'posts_per_page': posts_per_page}

    # Add Profile to context
    if request.user.is_authenticated:
        try:
            user_profile = get_object_or_404(Profile, user=request.user.id)
        except Exception as err:
            print(err)
            user_profile = None

        context['user_profile'] = user_profile

    return render(request, 'index.html', context)


def search_user(request):
    posts = []
    if 'q' in request.GET:
        posts = User.objects.filter(username__icontains=request.GET['q'])

    # Card groups
    posts = views_validations.separate_posts_into_quantity_groups(
        posts_list=posts, items_quantity=2)

    # Posts per page
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts_per_page = paginator.get_page(page)

    # Context
    context = {
        'url_context': 'index',
        'posts_per_page': posts_per_page}

    # Add Profile to context
    if request.user.is_authenticated:
        try:
            user_profile = get_object_or_404(Profile, user=request.user.id)
        except Exception as err:
            print(err)
            user_profile = None

        context['user_profile'] = user_profile

    return render(request, 'search_user.html', context)


def content(request, url_title, post_id):
    print(url_title)
    post = Post.objects.get(pk=post_id)  # type: ignore

    # Access (hidden content only for post.user.id)
    if request.user.id != post.user.id and not post.is_published:
        return redirect('index')

    # Profile
    try:
        user_profile = get_object_or_404(Profile, user=request.user.id)
    except Exception as err:
        print(err)
        user_profile = None

    context = {
        'url_context': 'content',
        'post': post,
        'user_profile': user_profile}

    return render(request, 'content.html', context)


def create(request, url_to_go_back):
    # Access
    if not request.user.is_authenticated:
        return redirect('index')

    # Profile
    try:
        user_profile = get_object_or_404(Profile, user=request.user.id)
    except Exception as err:
        print(err)
        user_profile = None

    # Post forms
    post_forms = PostForms

    # Context
    context = {
        'url_context': 'create',
        'url_to_go_back': url_to_go_back,
        'post_forms': post_forms,
        'message_err': None,
        'user_profile': user_profile}

    # Work on sent request
    if request.method == 'POST':
        # username: auth.get_user(request)
        post_content = request.POST['content']
        content_text = json.loads(post_content)['html'] if post_content else ''

        # Create post with sent request
        post = Post.objects.create(  # type: ignore
            user=get_object_or_404(User, pk=request.user.id),
            title=request.POST['title'],
            url_title=views_validations.normalize_title(request.POST['title']),
            image=request.FILES.get('image', 'post-default.svg'),
            summary=request.POST['summary'],
            content=content_text,
            category=request.POST['category'].lower(),
            publication_date=timezone.now(),
            is_published=True if 'is_published' in request.POST else False
        )

        # Save post
        post.save()

        # Go to url
        if 'is_published' not in request.POST:
            return redirect('dashboard_draft', request.user.username)

        if url_to_go_back == 'index':
            return redirect('index')

        return redirect('dashboard', request.user.username)

    return render(request, 'create.html', context)


def edit(request, url_title, post_id, url_to_go_back):
    # Post
    post_to_edit = get_object_or_404(Post, pk=post_id)

    # Access
    if not request.user.is_authenticated or (
            request.user.id != post_to_edit.user.id):
        return redirect('index')

    # Form
    post_forms = PostForms(
        initial={
            'user': get_object_or_404(User, pk=request.user.id),
            'title': post_to_edit.title,
            'url_title': post_to_edit.url_title,
            'image': post_to_edit.image.url,
            'summary': post_to_edit.summary,
            'content': post_to_edit.content,
            'category': post_to_edit.category,
            'publication_date': timezone.now(),
            'is_published': post_to_edit.is_published,
        })

    # Profile
    try:
        user_profile = get_object_or_404(Profile, user=request.user.id)
    except Exception as err:
        print(err)
        user_profile = None

    # Context
    context = {
        'url_context': 'edit',
        'url_to_go_back': url_to_go_back,
        'post_forms': post_forms,
        'post_id': post_id,
        'url_title': url_title,
        'message_err': None,
        'user_profile': user_profile}

    return render(request, 'edit.html', context)


def update(request, post_id):
    # Access
    if not request.user.is_authenticated:
        return redirect('index')

    # Work on sent request
    if request.method == 'POST':

        # Get post
        post = Post.objects.get(pk=post_id)  # type: ignore

        # Access
        if request.user.id != post.user.id:
            return redirect('index')

        post_content = request.POST['content']
        content_text = json.loads(post_content)['html'] if post_content else ''

        # Update post
        url_title = views_validations.normalize_title(request.POST['title'])

        post.title = request.POST['title']
        post.url_title = url_title
        post.summary = request.POST['summary']
        post.content = content_text
        post.category = request.POST['category']
        post.publication_date = timezone.now()
        post.is_published = True if 'is_published' in request.POST else False
        if 'image' in request.FILES:
            post.image = request.FILES['image']

        # Save updated post
        post.save()

        # Go to url
        return redirect('content', url_title, post_id)


def delete(request, url_to_go_back, post_id):
    # Access
    if not request.user.is_authenticated:
        return redirect('index')

    # Post
    post = get_object_or_404(Post, pk=post_id)

    # Delete
    post.delete()

    # Go to url
    if 'dashboard' in url_to_go_back:
        return redirect(url_to_go_back, request.user.username)
    return redirect('index')
