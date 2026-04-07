from django.contrib import admin

from .models import Capability, LandingContent, Lead


@admin.register(LandingContent)
class LandingContentAdmin(admin.ModelAdmin):
    """Одна запись с текстами лендинга."""

    fieldsets = (
        ('Hero', {'fields': ('hero_eyebrow', 'hero_title_line1', 'hero_title_accent', 'hero_subtitle')}),
        ('Блок заявки (pricing)', {'fields': ('pricing_eyebrow', 'pricing_title', 'pricing_text')}),
    )

    def has_add_permission(self, request):
        return not LandingContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Capability)
class CapabilityAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort_order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('sort_order', 'is_active')
    search_fields = ('title', 'text')
    ordering = ('sort_order', 'id')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'employee_count', 'status', 'source', 'created_at')
    list_filter = ('status', 'source', 'created_at')
    search_fields = ('email', 'name', 'phone', 'message')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'user_agent')
    fieldsets = (
        (None, {'fields': ('email', 'name', 'phone', 'employee_count', 'message', 'status')}),
        ('Внутреннее', {'fields': ('admin_notes', 'source', 'ip_address', 'user_agent')}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )

admin.site.site_header = 'Швей Метрикс — админка'
admin.site.site_title = 'Швей Метрикс'
