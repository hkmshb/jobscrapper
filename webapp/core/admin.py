from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Document, Description


admin.site.register(User, UserAdmin)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'is_active')


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'is_active')
