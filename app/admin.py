from django.contrib import admin
from .models import (Product, ProductTranslation, 
                     ProductImage, Category, Language, 
                     Certificates, Company, 
                     CategoryTranslation, Partners, Services, ServiceBase)
class BaseAdmin(admin.ModelAdmin):
    list_display=('title','description')


# Register your models here.
# admin.site.register(Services)

@admin.register(Services)
class ServicesAdmin(BaseAdmin):
    # list_display=(BaseAdmin.list_display+('description',))
    pass


admin.site.register(Language)
admin.site.register(Category)
admin.site.register(Partners)
admin.site.register(Product)
admin.site.register(ProductTranslation)
admin.site.register(ProductImage)
admin.site.register(Certificates)
admin.site.register(Company)
admin.site.register(CategoryTranslation)

