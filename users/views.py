from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator
from users.forms import SignUpForms, LoginForms
from webprofile.models import Post
import string

import views_validations


def dashboard(request, username):
    # request.user.username
    logged_in_user = get_object_or_404(User, username=username)
    posts = views_validations.separate_posts_into_quantity_groups(
        posts_list=Post.objects.order_by(  # type: ignore
            '-publication_date').filter(user=logged_in_user, is_published=True),
        items_quantity=2)

    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts_per_page = paginator.get_page(page)

    context = {
        'url': 'dashboard',
        'posts_per_page': posts_per_page,
        'logged_in_user': logged_in_user}
    return render(request, 'dashboard.html', context)


def dashboard_draft(request, username):
    logged_in_user = get_object_or_404(User, username=username)

    if (not request.user.is_authenticated
            or logged_in_user.id != request.user.id):
        return redirect('dashboard', username)

    posts = views_validations.separate_posts_into_quantity_groups(
        posts_list=Post.objects.order_by(  # type: ignore
            '-publication_date').filter(user=logged_in_user, is_published=False),
        items_quantity=3)

    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts_per_page = paginator.get_page(page)

    context = {
        'url': 'dashboard_draft',
        'posts_per_page': posts_per_page,
        'logged_in_user': logged_in_user}
    return render(request, 'dashboard_draft.html', context)


def settings(request, username):
    logged_in_user = get_object_or_404(User, username=username)

    if (not request.user.is_authenticated
            or logged_in_user.id != request.user.id):
        return redirect('dashboard', username)

    context = {
        'url': 'settings', 'logged_in_user': logged_in_user}
    return render(request, 'settings.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    user_forms = LoginForms
    context = {
        'url': 'login',
        'user_forms': user_forms,
        'message_err': None}

    if request.method == 'POST':
        # Username
        username = request.POST['username']
        if not username.strip():
            context['message_err'] = 'Preencha o nome de usuário'

        # Password
        password = request.POST['password']
        if not password.strip():
            context['message_err'] = 'Preencha a senha'

        # User
        if User.objects.filter(username=username).exists():
            user = auth.authenticate(
                request, username=username, password=password)

            # Auth
            if user is not None:
                auth.login(request, user)
                return redirect('index')

            # Errors
            if context['message_err']:
                return render(request, 'login.html', context)

    return render(request, 'login.html', context)


def logout(request):
    if not request.user.is_authenticated:
        return redirect('index')

    auth.logout(request)
    return redirect('index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    user_forms = SignUpForms
    context = {
        'url': 'signup',
        'user_forms': user_forms,
        'message_err': None}

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

        # Exists
        if User.objects.filter(username=username).exists():
            context['message_err'] = 'Usuário já cadastrado'
        if User.objects.filter(email=email).exists():
            context['message_err'] = 'Email já cadastrado'

        # Errors
        if context['message_err']:
            return render(request, 'signup.html', context)

        # User
        user = User.objects.create_user(
            username=username, first_name=name, email=email, password=password)
        user.save()

        return redirect('login')

    return render(request, 'signup.html', context)
