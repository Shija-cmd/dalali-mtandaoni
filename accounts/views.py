from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils.decorators import method_decorator
from properties.rate_limits import rate_limit
from .forms import UserRegisterForm


@method_decorator(
    rate_limit('web-login', limit=10, window=300),
    name='dispatch'
)
class UserLoginView(LoginView):

    template_name = 'accounts/login.html'

    def form_invalid(self, form):

        messages.error(
            self.request,
            'Invalid username or password. Please try again.'
        )

        return super().form_invalid(
            form
        )
    
    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        for field in form.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })

        return form


@rate_limit('web-register', limit=5, window=600)
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
