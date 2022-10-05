from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from profiles.models import Profile


def update_cover_image(request, url_to_go_back, url_username):
    # URL user
    url_user = get_object_or_404(User, username=url_username)

    if request.method == 'POST':
        # Get profile
        if create_profile_if_not_exist(request, url_user):
            profile = get_object_or_404(Profile, user=url_user.id)

            # Update image
            if 'cover_image' in request.FILES:
                profile.cover_image = request.FILES['cover_image']
                profile.save()

    if url_to_go_back == 'dashboard_draft':
        return redirect('dashboard_draft', url_user.username)
    return redirect('dashboard', url_user.username)


def clear_cover_image(request, url_to_go_back, url_username):
    # URL user
    url_user = get_object_or_404(User, username=url_username)

    if create_profile_if_not_exist(request, url_user):
        profile = get_object_or_404(Profile, user=url_user.id)

        profile.cover_image = 'cover-default.svg'
        profile.save()

    if url_to_go_back == 'dashboard_draft':
        return redirect('dashboard_draft', url_user.username)
    return redirect('dashboard', url_user.username)


def update_profile_image(request, url_to_go_back, url_username):
    # URL user
    url_user = get_object_or_404(User, username=url_username)

    if request.method == 'POST':
        # Get profile
        if create_profile_if_not_exist(request, url_user):
            profile = get_object_or_404(Profile, user=url_user.id)

            # Update image
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
                profile.save()

    if url_to_go_back == 'dashboard_draft':
        return redirect('dashboard_draft', url_user.username)
    return redirect('dashboard', url_user.username)


def clear_profile_image(request, url_to_go_back, url_username):
    # URL user
    url_user = get_object_or_404(User, username=url_username)

    if create_profile_if_not_exist(request, url_user):
        profile = get_object_or_404(Profile, user=url_user.id)

        profile.profile_image = 'profile-default.svg'
        profile.save()

    if url_to_go_back == 'dashboard_draft':
        return redirect('dashboard_draft', url_user.username)
    return redirect('dashboard', url_user.username)


def create_profile_if_not_exist(request, user) -> bool:
    try:
        get_object_or_404(Profile, user=user.id)
    except Exception as err:
        print(f'>>> Profile DoesNotExist! "Exception" error is: "{err}"')
    else:
        print(f'>>> Profile for user "{user.username}" found!')
        return True

    print('>>> Creating profile...')
    try:
        profile = Profile.objects.create(  # type: ignore
            user=get_object_or_404(User, pk=user.id),
            profile_image=request.FILES.get(
                'profile_image', 'profile-default.svg'),
            cover_image=request.FILES.get(
                'cover_image', 'cover-default.svg'),
        )
        profile.save()
    except Exception as err:
        print(f'>>> Profile cannot be created: "{err}"')
        return False
    else:
        print(f'>>> Profile for "{user.username}" has been created!')
        return True
