from django.urls import path
from .views import RedirectView

urlpatterns = [
    path('<slug:slug>/', RedirectView.as_view(), name='redirect'),
]