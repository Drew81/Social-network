from django.contrib import admin
from .models import Post, Details, UserProfile
# Register your models here.


admin.site.register(Post)
admin.site.register(Details)
admin.site.register(UserProfile)
