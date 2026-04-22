from django.db import models
from django.contrib.auth.models import User

class Shorturl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='short_urls')
    original_url = models.URLField(max_length=2000)
    slug = models.SlugField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    clickcount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.slug} -> {self.original_url[:50]}"
    
    class Meta:
        ordering = ['-created_at']