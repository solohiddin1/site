from django.shortcuts import render
from rest_framework import viewsets
from .models import Certificates, Language, Category, Product, ProductTranslation, ProductImage, Company, Partners
from .serilializers import (
    LanguageSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductTranslationSerializer,
    ProductImageSerializer,
    CertificatesSerializer,
    CompanySerializer,
    CategoryTranlationSerializer,
    PartnersSerializer
)
from rest_framework.decorators import APIView
from rest_framework.response import Response

# Create your views here.

# class CategoryTranslationSerializer(APIView)

class PartnersView(APIView):
    def get(self,request):
        partners = Partners.objects.all()
        serializer = PartnersSerializer(partners, many=True)
        return Response(serializer.data)
    

class CertificatesViewSet(APIView):
    def get(self, request):
        certificates = Certificates.objects.all()
        serializer = CertificatesSerializer(certificates, many=True,context={'request': request})
        return Response(serializer.data)

class CompanyViewSet(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

class LanguageViewSet(APIView):
    def get(self, request):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)


class CategoryViewSet(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProductViewSet(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductTranslationViewSet(APIView):
    def get(self, request):
        translations = ProductTranslation.objects.all()
        serializer = ProductTranslationSerializer(translations, many=True)
        return Response(serializer.data)
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


class ProductImageView(APIView):
    def get(self,request):
        product_id = self.request.query_params.get('product')
        images = ProductImage.objects.filter(product_id=product_id)
        print(images)
        serializer = ProductImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)


class ProductTranslationViewDetail(APIView):
    def get(self, request):
        product_id = self.request.query_params.get('product')
        language_id = self.request.query_params.get('language')
        product =  ProductTranslation.objects.filter(product_id=product_id, language_id=language_id)
        print(product)
        print('request entered to product tranlation')
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
                print("entered to default")
                serializer = ProductTranslationSerializer(default_product)
                return Response(serializer.data)
        return Response({"detail": " No product translation found"},status=200)


class CategoriesDetailView(APIView):
    def get(self,request,pk):
        data = Category.objects.filter(pk=pk).first()

        serializer = CategorySerializer(data)
        return Response(serializer.data,status=200)
