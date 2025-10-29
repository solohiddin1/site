from django.shortcuts import render
from rest_framework import viewsets
from .models import Certificates, Language, Category, Product, ProductTranslation, ProductImage, Company
from .serilializers import (
    LanguageSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductTranslationSerializer,
    ProductImageSerializer,
    CertificatesSerializer,
    CompanySerializer,
)
from rest_framework.decorators import APIView
from rest_framework.response import Response

# Create your views here.

class CertificatesViewSet(viewsets.ModelViewSet):
    queryset = Certificates.objects.all()
    serializer_class = CertificatesSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

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


class ProductByCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category')  # from ?category=1
        if category_id is not None:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.none()

class ProductView(APIView):
    def get(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        serializer = ProductSerializer(product)

        return Response(serializer.data)
    

class ProductTranslationViewDetail(APIView):
    def get(self, request):
        product_id = self.request.query_params.get('product')
        language_id = self.request.query_params.get('language')
        product =  ProductTranslation.objects.filter(product_id=product_id, language_id=language_id)
        print(product)
        if product.exists():
            print("here1")
            serializer = ProductTranslationSerializer(product,many=True)
            return Response(serializer.data)
        else:
            print("here2")
            default_lang = Language.objects.get(is_default=True)
            print(default_lang)
            default_product = ProductTranslation.objects.filter(product_id=product_id, language_id=default_lang.id).first()
            if default_product:
                serializer = ProductTranslationSerializer(default_product)
                return Response(serializer.data)
        return Response(status=404)

