from django.contrib import admin

from core.models import Category


@admin.register(Category)
class OptionMenuAdmin(admin.ModelAdmin):
    list_display = ('name',)


