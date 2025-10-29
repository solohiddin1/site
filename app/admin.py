from django.contrib import admin
from .models import (Product, ProductTranslation, ProductImage, Category, Language, Certificates, Company, CategoryTranslation)
# Register your models here.

admin.site.register(Language)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductTranslation)
admin.site.register(ProductImage)
admin.site.register(Certificates)
admin.site.register(Company)
admin.site.register(CategoryTranslation)
