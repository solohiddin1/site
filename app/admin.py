from django.contrib import admin
from .models import (Product, ProductImage, Category,
                     Certificates, Company, 
                     Partners, Services)
from parler.admin import TranslatableAdmin


# Register your models here.
# admin.site.register(Services)

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display=('name','id','image_thumbnail')
    search_fields=('translations__name',)
    # prepopulated_fields = {'slug': ('name',)}

    def image_thumbnail(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50"/>'
        return ''
    image_thumbnail.allow_tags = True
    image_thumbnail.short_description='Image preview'

class ProductInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt', 'ordering', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50"/>'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    inlines = [ProductInline]
    list_display = ('name', 'sku', 'price', 'category', 'id')
    search_fields = ('translations__name', 'sku')
    list_filter = ('category',)
    # prepopulated_fields = {"translations__slug": ("translations__name",)}


@admin.register(Certificates)
class CertificatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'ordering')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50"/>'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'


@admin.register(Company)
class CompanyAdmin(TranslatableAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('translations__name',)


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50"/>'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = 'Logo'


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'location_url')
    list_filter = ('location',)
    search_fields = ('title', 'description')

# admin.site.register(Category)
# admin.site.register(Partners)
# admin.site.register(Product)
# admin.site.register(ProductImage)
# admin.site.register(Certificates)
# admin.site.register(Company)