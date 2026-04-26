from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Shorturl
from .serializers import ShorturlSerializer

class ShorturlView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        urls = Shorturl.objects.filter(user=request.user)
        serializer = ShorturlSerializer(urls, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ShorturlSerializer(data=request.data, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShorturlDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            url = Shorturl.objects.get(pk=pk, user=request.user)
            url.delete()
            return Response({'message':'URL deleted Successfully'}, status=status.HTTP_200_OK)
        except Shorturl.DoesNotExist:
            return Response({'error': 'URL not found'}, status=status.HTTP_404_NOT_FOUND)