from django.shortcuts import render
from rest_framework import viewsets
from .models import Language, Category, Product, ProductTranslation, ProductImage
from .serilializers import (
    LanguageSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductTranslationSerializer,
    ProductImageSerializer,
)

# Create your views here.

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductTranslationViewSet(viewsets.ModelViewSet):
    queryset = ProductTranslation.objects.all()
    serializer_class = ProductTranslationSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
