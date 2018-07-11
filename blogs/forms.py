from django import forms
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Blog,Category


class UserRegistrationForm(forms.Form):
    """ User registration form """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control mt-4','placeholder':'Username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control mt-4','placeholder':'Password'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control mt-4','placeholder':'Confirm password'}))

    def clean_confirm_password(self):
        """ Validate if password is equal to confir_password
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password did not match.')

        return confirm_password


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already taken.')

        return email


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')

        return  username
        

    def save(self):
        user = User()
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user


class LoginForm(forms.ModelForm):
    """ Login view form. """

    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model=User
        fields=('username','password')

    def clean(self):
        current_user = None
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username,password=password)
        if not user:
            raise forms.ValidationError('Login failed. Please try again.')
        else:
            self.current_user = user


class BlogForm(forms.ModelForm):
    """ Blog Form """

    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Title'}))
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control mb-4', 'placeholder': 'Content'}))
    category = forms.ModelChoiceField(queryset = Category.objects.all(),widget=forms.Select(attrs={'class' : 'form-control my-4'}))
    class Meta:
        model= Blog
        fields =('title','content','cover_image','category')

    def save(self,user,commit=True):

        instance = super(BlogForm,self).save(commit=False)
        if commit:
            instance.owner = user
            instance.save()
        return