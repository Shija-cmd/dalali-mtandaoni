from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import UserRegisterForm


class UserLoginView(LoginView):

    template_name = 'accounts/login.html'


def register(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            form.save()
            
            messages.success(
                request,
                'Account created successfully. Please log in.'
            )

            return redirect('login')

    else:

        form = UserRegisterForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


def user_logout(request):

    logout(request)
    
    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect('home')