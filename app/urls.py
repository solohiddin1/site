from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (LanguageViewSet, CategoryViewSet, 
    ProductImageViewSet, ProductViewSet, ProductTranslationViewSet, 
    ProductImageViewSet, CertificatesViewSet, CompanyViewSet, ProductByCategoryViewSet, ProductView,
    ProductTranslationViewDetail, ProductImageView)

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'categories', CategoryViewSet)
# router.register(r'products', ProductViewSet)
router.register(r'product-translations', ProductTranslationViewSet)
# router.register(r'product-images', ProductImageViewSet)
router.register(r'certificates', CertificatesViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductByCategoryViewSet.as_view({'get': 'list'}), name='product-images-list'),
    path('products/<int:pk>/', ProductView.as_view(), name='product-images'),

    path('product-images/', ProductImageView.as_view(), name='product-detail'),

    path('product-translations/', ProductTranslationViewDetail.as_view(), name='product-translation-detail'),
    # product-translations
    # path('products/')
]