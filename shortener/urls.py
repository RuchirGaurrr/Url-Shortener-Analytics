from django.urls import path
from .views import ShorturlView, ShorturlDetailView

urlpatterns = [
    path('urls/', ShorturlView.as_view(), name='short-urls'),
    path('urls/<int:pk>/', ShorturlDetailView.as_view(), name='short-url-detail'),
]