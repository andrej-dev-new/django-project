from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'bio')
