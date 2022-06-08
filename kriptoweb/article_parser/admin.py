from django.contrib import admin

# Register your models here.
from .models import Sources, Patterns

admin.site.register(Sources)
admin.site.register(Patterns)
