from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from authy.form import UserUpdateForm, ProfileUpdateForm
from authy.models import Profile


def register(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already used")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already used")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('register')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')
    else:
        context = {
        }
        return render(request, 'authy/register.html', context)


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    context = {
        'profile': profile
    }

    return render(request, 'authy/profile.html', context)


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # return redirect(f'profile', user.username)
            return redirect(f'index')
        else:
            messages.info(request, "Credentials Invalid")
            return redirect(f'login')
    else:
        context = {
        }
        return render(request, 'authy/login.html', context)


def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        # u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            # u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(f'profile', user.username)
        else:
            messages.success(request, f'All fields are required! Make sure you fill all')
            return redirect('edit_profile', user.username)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        # 'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'authy/edit_profile.html', context)