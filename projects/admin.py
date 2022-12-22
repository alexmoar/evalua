from django.contrib import admin

# Register your models here.
from projects.models import Score


@admin.register(Score)
class OptionMenuAdmin(admin.ModelAdmin):
    list_display = ('score', 'evaluator', 'project',)

    list_filter = ('evaluator',)


