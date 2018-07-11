from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog,Category
from .forms import UserRegistrationForm,LoginForm,BlogForm

class IndexView(TemplateView):
    """ Registration and index page
    """
    template_name = 'blogs/index.html'
    
    categories = Category.objects.all()

    def get(self, *args, **kwargs):
        form = UserRegistrationForm(self.request.GET or None)
        my_blog_list = {}
        blog_list = Blog.objects.all().order_by('-date_added')
        if self.request.user.is_authenticated:
            my_blog_list = Blog.objects.filter(owner=self.request.user).order_by('-date_added')
        categories = Category.objects.all().order_by('name')
        return render(self.request,self.template_name,{
            'blog_list' : blog_list,
            'my_blog_list' : my_blog_list,
            'form' : form,
            'categories' : self.categories,
        })

    def post(self, *args, **kwargs):
        form = UserRegistrationForm(self.request.POST)
        blog_list = Blog.objects.all().order_by('-date_added')
        if form.is_valid():
            user = form.save()
            user = authenticate(username = form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(self.request, user)

            my_blog_list = Blog.objects.filter(owner=self.request.user).order_by('-date_added')
            
            return render(self.request, self.template_name, { 
                'blog_list' : blog_list,
                'my_blog_list' : my_blog_list,
                'categories' : self.categories,
            })

        else:
            return render(self.request,self.template_name,{ 'blog_list': blog_list, 'form' : form })


class LoginView(TemplateView):
    """ User login 
    """
    template_name = "blogs/index.html"

    def get(self,*args,**kwargs):
        return render(self.request,self.template_name,{})

    def post(self,*args,**kwargs):
        form = LoginForm(self.request.POST)
        if(form.is_valid()):
            login(self.request, form.current_user)
        else:
            errors= {} 
            blog_list = Blog.objects.all().order_by('-date_added')

            for error in form.errors:
                errors[error] = form.errors[error]

            return render(self.request,self.template_name,{ 
                'blog_list' : blog_list,
                'login_errors' : errors
                })
        return HttpResponseRedirect(reverse('blogs:index'))


class AddBlogView(LoginRequiredMixin,TemplateView):
    """ Add a new blog
    """
    template_name = 'blogs/form.html'

    def get(self, *args, **kwargs):
        form = BlogForm(self.request.GET or None)
        form.owner = self.request.user
        categories = Category.objects.all().order_by('name')

        return render(self.request,self.template_name,{
            'form' : form,
            'label': 'ADD BLOG',
        })

    def post(self, *args,**kwargs):
        form = BlogForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            form.save(self.request.user)
            return HttpResponseRedirect(reverse('blogs:index'))
        
        else:
            return render(self.request,self.template_name,{
                'form':form,
                'label' : "ADD BLOG",
            })


class LogoutView(View):
    """ Logout a user
    """
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('blogs:index'))


class EditBlogView(LoginRequiredMixin,TemplateView):
    """ Eit a blog
    """
    template_name = 'blogs/form.html'

    def  get(self,*args,**kwargs):
        blog = get_object_or_404(Blog,pk=self.kwargs.get('pk'),owner=self.request.user)
        form = BlogForm(self.request.GET or None, instance=blog)

        return render(self.request,self.template_name,{'form':form, 'label' : 'EDIT BLOG'})

    def post(self,*args,**kwargs):
        blog = get_object_or_404(Blog,pk=self.kwargs.get('pk'),owner=self.request.user)
        form = BlogForm(self.request.POST, self.request.FILES, instance=blog)

        if form.is_valid():
            form.save(user=self.request.user)
            return HttpResponseRedirect(reverse('blogs:index'))
        
        else:
            categories = Category.objects.all().order_by('name')
            return render(self.request,self.template_name,{
                'form' : form,
                'label' : "EDIT BLOG"
            })


class BlogView(TemplateView):
    """ View a blog
    """
    template_name = 'blogs/blog.html'

    def get(self,*args, **kwargs):
        categories = Category.objects.all().order_by('name')
        blog = get_object_or_404(Blog,pk=self.kwargs.get('pk'))
        return render(self.request,self.template_name,{
            'categories' : categories,
            'blog_info' : blog
        })
    

class CategoryView(TemplateView):
    """ Display blog per category
    """
    template_name = 'blogs/category.html'
    category_list = Category.objects.all().order_by('name')

    def get(self,*args,**kwargs):
        category = get_object_or_404(Category,pk=kwargs.get('pk'))
        blog_list = Blog.objects.filter(category=category)

        return render(self.request,self.template_name,{
            'blog_list' : blog_list,
            'category_info' : category,
            'category_list' : self.category_list,
            })


class DeleteBlogView(View):
    """ Deletes a blog 
    """
    def get(self, *args, **kwargs):
        blog = get_object_or_404(Blog,pk=kwargs.get('pk'),owner = self.request.user)
        blog.delete()
        return HttpResponseRedirect(reverse('blogs:index'))











