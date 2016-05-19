from django.contrib import admin

# Register your models here.
from ecs.elections.models import Election, Result

admin.site.register(Election)
admin.site.register(Result)
