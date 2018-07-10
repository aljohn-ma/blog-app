from django import forms
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Blog,Category


class UserRegistrationForm(forms.ModelForm):
    """ User registration form """

    confirm_password = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

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
            raise forms.ValidationError('Email is already taken')
        return email

    def save(self, commit=True):
        """save user
        """
        instance = super(UserRegistrationForm, self).save(commit=False)
        if commit:
            
            instance.set_password(self.cleaned_data.get('password'))
            instance.save()

        return instance

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

    selected_category = forms.IntegerField(required=True)
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Title'}))
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control mb-4', 'placeholder': 'Content'}))
    
    class Meta:
        model= Blog
        fields =('title','content','cover_image')

    def save(self,**kwargs):
        """ Save blog """
        user = kwargs.get('user')
        commit = kwargs.get('commit')
        instance = super(BlogForm,self).save(commit=False)
        if commit:
            try:
                category_id = Category.objects.get(pk=self.cleaned_data.get('selected_category'))

            except Category.DoesNotExist:
                category_id = None

            instance.owner = user
            instance.category = category_id 
            instance.save()
        return

    def build_errors(self,form):
        errors= {}        
        for error in form.errors:
            errors[error] = form.errors[error]
        
        return errors


