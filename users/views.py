from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator
from users.forms import SignUpForms, LoginForms
from webprofile.models import Post
import string

import views_validations


def dashboard(request, username):
    # URL user
    url_user = get_object_or_404(User, username=username)

    # Posts
    posts = views_validations.separate_posts_into_quantity_groups(
        posts_list=Post.objects.order_by(  # type: ignore
            '-publication_date').filter(
            user=url_user, is_published=True), items_quantity=2)

    # Posts per page
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts_per_page = paginator.get_page(page)

    # Context
    context = {
        'url': 'dashboard',
        'url_user': url_user,
        'posts_per_page': posts_per_page}

    return render(request, 'dashboard.html', context)


def dashboard_draft(request, username):
    # URL user
    url_user = get_object_or_404(User, username=username)

    # Draft access
    if not request.user.is_authenticated or request.user.id != url_user.id:
        return redirect('dashboard', username)

    # Posts
    posts = views_validations.separate_posts_into_quantity_groups(
        posts_list=Post.objects.order_by(  # type: ignore
            '-publication_date').filter(user=url_user, is_published=False),
        items_quantity=3)

    # Posts per page
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts_per_page = paginator.get_page(page)

    # Context
    context = {
        'url': 'dashboard_draft',
        'url_user': url_user,
        'posts_per_page': posts_per_page}

    return render(request, 'dashboard_draft.html', context)


def settings(request, username):
    # URL user
    url_user = get_object_or_404(User, username=username)

    # Settings access
    if not request.user.is_authenticated or request.user.id != url_user.id:
        return redirect('dashboard', username)

    # Context
    context = {
        'url': 'settings',
        'url_user': url_user}

    return render(request, 'settings.html', context)


def login(request):
    # Login access
    if request.user.is_authenticated:
        return redirect('index')

    # User forms
    user_forms = LoginForms

    # Context
    context = {
        'url': 'login',
        'user_forms': user_forms,
        'message_err': None}

    # Work on sent request
    if request.method == 'POST':

        # Username
        username = request.POST['username']
        if not username.strip():
            context['message_err'] = 'Preencha o nome de usuário'

        # Password
        password = request.POST['password']
        if not password.strip():
            context['message_err'] = 'Preencha a senha'

        # User exists
        if User.objects.filter(username=username).exists():

            # Get the user
            user = auth.authenticate(
                request, username=username, password=password)

            # Authenticate the user
            if user is not None:
                auth.login(request, user)
                return redirect('index')

            # Errors: insert on context
            if context['message_err']:
                return render(request, 'login.html', context)

    return render(request, 'login.html', context)


def logout(request):
    # Logout access
    if not request.user.is_authenticated:
        return redirect('index')

    # Logout the user
    auth.logout(request)

    return redirect('index')


def signup(request):
    # Signup access
    if request.user.is_authenticated:
        return redirect('index')

    # User forms
    user_forms = SignUpForms

    # Context
    context = {
        'url': 'signup',
        'user_forms': user_forms,
        'message_err': None}

    # Work on sent request
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        valid_chars = list(string.ascii_letters + string.digits)

        # Name
        if not name.strip():
            context['message_err'] = 'Preencha o nome'
        elif len(name) >= 200:
            context['message_err'] = 'Nome muito longo'
        elif any(char not in valid_chars + [' '] for char in name):
            context['message_err'] = 'Nome nulo! Use letras, números e espaços'

        # Username
        elif not username.strip():
            context['message_err'] = 'Preencha o nome de usuário'
        elif not username.isalpha():
            context['message_err'] = 'Nome de usuário só pode conter letras'

        # Email
        elif not email.strip():
            context['message_err'] = 'Preencha o email'

        # Password
        elif not password.strip() or not password_confirm.strip():
            context['message_err'] = 'Preencha a senha'
        elif password != password_confirm:
            context['message_err'] = 'As senhas não correspondem'
        elif (len(password) < 8 or
              all(char.isalpha() for char in password) or
              all(char.isdigit() for char in password) or
              any(char not in valid_chars for char in password)):
            context['message_err'] = 'Senha inválida'

        # User exists
        if User.objects.filter(username=username).exists():
            context['message_err'] = 'Usuário já cadastrado'
        if User.objects.filter(email=email).exists():
            context['message_err'] = 'Email já cadastrado'

        # Errors -> exit
        if context['message_err']:
            return render(request, 'signup.html', context)

        # Create the user
        user = User.objects.create_user(
            username=username, first_name=name, email=email, password=password)

        # Save created user
        user.save()

        # Go to 'Login'
        return redirect('login')

    return render(request, 'signup.html', context)
