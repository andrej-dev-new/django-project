from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView


from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Welcome to EventHub, your account was created!")
        login(self.request, user)
        return super().form_valid(form)

class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')  

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('dashboard:home')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'dashboard/dashboard.html', {'profile_form': form})
