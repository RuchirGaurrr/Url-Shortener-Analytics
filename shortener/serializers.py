from rest_framework import serializers
from .models import Shorturl
from .utils import generate_slug

class ShorturlSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    original_url = serializers.URLField()
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Shorturl
        fields = ['id', 'original_url', 'slug', 'short_url', 'clickcount', 'is_active', 'created_at']
        read_only_fields = ['clickcount', 'is_active', 'created_at']
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/{obj.slug}/')
    
    def create(self, validated_data):
        original_url = validated_data.get('original_url')
        slug = validated_data.get('slug') or generate_slug(original_url)
        user = self.context.get('request').user
        return Shorturl.objects.create(
            user = user,
            original_url = original_url,
            slug = slug
        )