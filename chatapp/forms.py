#chatapp/forms.py
from django.contrib.auth import (
    authenticate,
    get_user_model
)
from django import forms


User = get_user_model()

# User login form
class UserLoginForm(forms.Form):
    username = forms.CharField(
                widget=forms.TextInput(
                   attrs={
                       'id':'login',
                       'class':'fadeIn second',
                       'name':"login",
                       'placeholder':'username'
                }))
    password = forms.CharField(
                widget=forms.PasswordInput(
                   attrs={
                       'id':'password',
                       'class':'fadeIn third',
                       'name':"login",
                       'placeholder':'password'
                }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist or password incorrect')

        return super(UserLoginForm, self).clean(*args, **kwargs)

# User registration form
class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(
                widget=forms.TextInput(
                    attrs={
                        'id':'login',
                        'class':'fadeIn second',
                        'name':"login",
                        'placeholder':'username'
                }))
    password = forms.CharField(
                widget=forms.PasswordInput(
                    attrs={
                        'id':'password',
                        'class':'fadeIn third',
                        'name':"login",
                        'placeholder':'password'
                        }))
    confirm_password = forms.CharField(
                        widget=forms.PasswordInput(
                            attrs={
                                'id':'password',
                                'class':'fadeIn third',
                                'name':"login",
                                'placeholder':'confirm password'
                        }))

    class Meta:
        model = User
        fields = [
            'username',
            'confirm_password',
            'password'
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        qs = User.objects.filter(username=username)

        if qs.exists():
            raise forms.ValidationError("User already exists")
        
        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password must match")
        
        return super(UserRegisterForm, self).clean(*args, **kwargs)