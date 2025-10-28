from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LanguageViewSet, CategoryViewSet, ProductImageViewSet, ProductViewSet, ProductTranslationViewSet, ProductImageViewSet

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-translations', ProductTranslationViewSet)
router.register(r'product-images', ProductImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]