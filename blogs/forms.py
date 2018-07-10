from django import forms
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Blog,Category


class UserRegistrationForm(forms.ModelForm):
    """ User registration form """

    # username = forms.CharField()
    # email = forms.EmailField()
    # password = forms.CharField()
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
    username = forms.CharField()
    password = forms.CharField()

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

    title   = forms.CharField(required=True)
    content = forms.CharField(required=True)
    selected_category = forms.IntegerField(required=True)
    blog_id = forms.IntegerField(required=False)
    cover_image = forms.FileField(required=True)

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

            """ Check if blog_id is > 0 """
            existing_blog_id = self.cleaned_data.get('blog_id')
            if existing_blog_id:
                try :
                    edit_blog = get_object_or_404(Blog,pk=existing_blog_id)
                    edit_blog.owner = user
                    edit_blog.category = category_id
                    edit_blog.title = instance.title
                    edit_blog.content = instance.content
                    edit_blog.cover_image = instance.cover_image
                    edit_blog.date_updated = datetime.datetime.now()
                    edit_blog.save()

                except Blog.DoesNotExist:
                    return
            else:
                instance.owner = user
                instance.category = category_id 
                instance.save()
        return

    def build_errors(self,form):
        errors= {}        
        for error in form.errors:
            errors[error] = form.errors[error]
        
        return errors


