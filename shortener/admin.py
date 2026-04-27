from django.contrib import admin
from .models import Shorturl

@admin.register(Shorturl)
class ShorturlAdmin(admin.ModelAdmin):
    list_display = ['slug', 'user', 'original_url', 'clickcount', 'is_active', 'created_at']
    search_fields = ['slug', 'original_url', 'user__username']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['clickcount', 'created_at']
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')