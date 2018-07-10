from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blogs'

urlpatterns = [
    path('blogs/',views.IndexView.as_view(), name='index'),
    path('blogs/register/', views.RegistrationView.as_view(), name='register'),
    path('blogs/login/', views.LoginView.as_view(), name='login'),
    path('blogs/add/', views.AddBlogView.as_view(), name='add'),
    path('blogs/edit/<int:pk>', views.EditBlogView.as_view(), name='edit'),
    path('blogs/view/<int:pk>', views.BlogView.as_view(), name='view'),
    path('blogs/category/<int:pk>',views.CategoryView.as_view(), name='category'),
    path('blogs/delete/<int:pk>', views.delete, name='delete'),
    path('logout/',views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
