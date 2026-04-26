from django.urls import path
from .views import RedirectView, AnalyticsView

urlpatterns = [
    path('<slug:slug>/', RedirectView.as_view(), name='redirect'),
    path('api/analytics/<slug:slug>/', AnalyticsView.as_view(), name='analytics'),
]