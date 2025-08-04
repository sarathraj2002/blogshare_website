from django.contrib import admin

from my_app.models import BlogPost,Profile,Comment

# Register your models here.
admin.site.register(Profile)
admin.site.register(BlogPost)
admin.site.register(Comment)