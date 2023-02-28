from django.contrib import admin

# Register your models here.
from .models import Videos

# registering the Videos to the admin site
admin.site.register(Videos)