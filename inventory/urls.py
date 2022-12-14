'''
API URLs register here
'''

# book/inventory/urls.py : API urls.py

from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'wishlist', views.WishlistViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'available', views.UpdateAvailability)
router.register(r'report', views.GenerateReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest'))
]