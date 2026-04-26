from  django.shortcuts import redirect
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shortener.models import Shorturl
from rest_framework.permissions import IsAuthenticated
from shortener.models import Shorturl
from .models import Click
from .tracker import log_click

class RedirectView(APIView):
    permission_classes =[]

    def get(self, request, slug):
        #check in redis cache
        cached_url = cache.get(slug)

        if cached_url:
            #cache HIT
            try:
                short_url = Shorturl.objects.get(slug = slug)
                log_click(request, short_url)
            except Shorturl.DoesNotExist:
                pass
            return redirect(cached_url)
        #cache MISS
        try:
            short_url = Shorturl.objects.get(slug = slug, is_active=True)
        except Shorturl.DoesNotExist:
            return Response({'message':'URL not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        #Store in Redis forf uture use
        cache.set(slug, short_url.original_url, timeout=86400)
        log_click(request, short_url)
        return redirect(short_url.original_url)

class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            short_url = Shorturl.objects.get(slug = slug, user = request.user)
        except Shorturl.DoesNotExist:
            return Response({'message':'URL not found'}, status=status.HTTP_404_NOT_FOUND)
        
        clicks = Click.objects.filter(short_url=short_url)
        
        by_device = {}
        by_browser = {}
        by_country = {}

        for click in clicks:
            by_device[click.device] = by_device.get(click.device, 0) + 1
            by_browser[click.browser] = by_browser.get(click.browser, 0) + 1
            by_country[click.country] = by_country.get(click.country, 0) + 1
        
        return Response({
            'slug': slug,
            'total_clicks': short_url.clickcount,
            'by_device': by_device,
            'by_browser': by_browser,
            'by_country': by_country
        })
