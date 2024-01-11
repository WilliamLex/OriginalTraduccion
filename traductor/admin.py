from django.contrib import admin
from .models import TipoTraduccion, Traduccion, Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ('created', )
admin.site.register(TipoTraduccion)
admin.site.register(Traduccion)

admin.site.register(Task, TaskAdmin)
