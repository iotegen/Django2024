from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,User
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow
from .forms import ProfileForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('register')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    is_following = Follow.objects.filter(follower=request.user, following=user).exists() 

    is_own_profile = request.user == user

    return render(request, 'profile.html', {'user_profile': user.profile,'user':user,'is_following':is_following,'is_own_profile':is_own_profile})

@login_required
def edit_profile(request,username):
    user = get_object_or_404(User,username=username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form,'user':user})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow != request.user:  # Prevent self-follow
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=user_to_follow.username)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    if user_to_unfollow != request.user:  # Prevent self-unfollow
        Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=user_to_unfollow.username)
