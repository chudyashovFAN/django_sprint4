from django.contrib import admin

from .models import Location, Post, Category


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Location)
