from django.db import models
from shortener.models import Shorturl

class Click(models.Model):
    short_url = models.ForeignKey(Shorturl, on_delete=models.CASCADE, related_name='clicks')
    timestamp = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Click on {self.short_url.slug} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
