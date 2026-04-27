from django.contrib import admin
from .models import Click

@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ['short_url', 'timestamp', 'device', 'browser', 'country', 'ip_address']
    search_fields = ['short_url__slug', 'country', 'browser']
    list_filter = ['device', 'browser', 'country']
    readonly_fields = ['short_url', 'timestamp', 'ip_address', 'device', 'browser', 'country']
    list_per_page = 50

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('short_url__user')