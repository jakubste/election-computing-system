from django.contrib import admin

# Register your models here.
from ecs.elections.models import Election

admin.site.register(Election)
