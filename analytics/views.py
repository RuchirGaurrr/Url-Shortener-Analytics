from  django.shortcuts import redirect
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shortener.models import Shorturl

class RedirectView(APIView):
    permission_classes =[]

    def get(self, request, slug):
        #check in redis cache
        cached_url = cache.get(slug)

        if cached_url:
            #cache HIT
            return redirect(cached_url)
        #cache MISS
        try:
            short_url = Shorturl.objects.get(slug = slug, is_active=True)
        except Shorturl.DoesNotExist:
            return Response({'message':'URL not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        #Store in Redis forf uture use
        cache.set(slug, short_url.original_url, timeout=86400)
        return redirect(short_url.original_url)