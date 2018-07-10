from django.contrib import admin

from .models import Blog, Category

class BlogAdmin(admin.ModelAdmin):
    list_display = ('owner','title','content','date_added','date_updated')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields =('name',)

admin.site.register(Blog,BlogAdmin)
admin.site.register(Category,CategoryAdmin)


