from .models import User
from django import forms
from django.core.mail import send_mail



class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This {email} is already registered.')
        return email

    def clean_password(self):
        password: str = self.data.get('password')
        confirm_password: str = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Please enter the same password')
        return self.cleaned_data['password']

    def save(self, commit=True):
        user = super(RegisterModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.is_superuser = True
        user.is_staff = True

        if commit:
            user.save()

        return user

