from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog,Category
from .forms import UserRegistrationForm,LoginForm,BlogForm

class IndexView(generic.ListView):
    """docstring for IndexView"""
    template_name = 'blogs/index.html'
    # context_object_name = 'blog_list'
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['blog_list'] = Blog.objects.all().order_by('-date_added')
        context['my_blog_list'] = Blog.objects.filter(owner=self.request.user.id).order_by('-date_added')
        context['categories'] = Category.objects.all().order_by('name')
        return context

    def get_queryset(self):
        pass


class RegistrationView(TemplateView):

    """ View for user registration
    """
    template_name = "blogs/index.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {})

    def post(self, *args, **kwargs):
        form = UserRegistrationForm(self.request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username = form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(self.request, user)
            return render(self.request, self.template_name, {})
        else:
            errors= {}            
            for error in form.errors:
                errors[error] = form.errors[error]
            return render(self.request,self.template_name,{ 'errors' : errors })


class LoginView(TemplateView):
    
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

            del errors['__all__']
            errors['status']= form.errors['__all__']

            return render(self.request,self.template_name,{ 
                'blog_list' : blog_list,
                'login_errors' : errors
                })
        
        next_page = kwargs.get('next')
        if  next_page is not None:
            return HttpResponseRedirect(reverse('blogs:{}'.format(next_page)))
        return HttpResponseRedirect(reverse('blogs:index'))


class AddView(LoginRequiredMixin,TemplateView):

    template_name = 'blogs/add.html'

    def get(self, *args, **kwargs):
        categories = Category.objects.all().order_by('name')

        return render(self.request,self.template_name,{'label': 'ADD BLOG','categories' : categories })

    def post(self, *args,**kwargs):
        return render(self.request,self.template_name,{})


class LogoutView(View):

    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('blogs:index'))


class SaveBlogView(TemplateView):

    template_name = 'blogs/add.html'

    def get(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('blogs:index'))
    def post(self,*args,**kwargs):
        form_data = BlogForm(self.request.POST, self.request.FILES)

        if form_data.is_valid():

            form_data.save(user=self.request.user,pk=kwargs.get('pk'),commit=True)
            return HttpResponseRedirect(reverse('blogs:index'))
        
        else:
            label = "ADD BLOG"
            if kwargs.get('pk'):
                label = "EDIT BLOG"
            errors = form_data.build_errors(form_data)
            categories = Category.objects.all().order_by('name')
            return render(self.request,self.template_name,{
                'errors' : errors,
                'categories' : categories,
                'blog': form_data.cleaned_data,
                'label' : label
            })


class EditView(LoginRequiredMixin,TemplateView):
    template_name = 'blogs/add.html'

    def  get(self,*args,**kwargs):
        categories = Category.objects.all().order_by('name')
        blog = Blog.objects.get(pk=self.kwargs.get('pk'))
        return render(self.request,self.template_name,{
            'label' : 'EDIT BLOG',
            'categories' : categories,
            'blog' : blog
        })


class BlogView(TemplateView):

    template_name = 'blogs/blog.html'

    def get(self,*args, **kwargs):
        categories = Category.objects.all().order_by('name')
        blog = Blog.objects.get(pk=self.kwargs.get('pk'))
        return render(self.request,self.template_name,{
            'categories' : categories,
            'blog_info' : blog
        })
    

class CategoryView(TemplateView):
    """docstring for CategoryView"""
    template_name = 'blogs/category.html'

    def get(self,*args,**kwargs):
        try:
            category_list = Category.objects.all().order_by('name')
            category = Category.objects.get(pk=self.kwargs.get('pk'))
            blog_list = Blog.objects.filter(category=category)

        except:
            category_list = {}
            category = {}
            blog_list = {}

        return render(self.request,self.template_name,{
            'blog_list' : blog_list,
            'category_info' : category,
            'category_list' : category_list,
            })


        
def delete(request,pk):
    Blog.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('blogs:index'))










