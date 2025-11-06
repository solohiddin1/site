from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
import uuid

def get_unique_code():
    return str(uuid.uuid4().int)[:4]

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True,)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True,)

    class Meta:
        abstract = True


class Category(BaseModel, TranslatableModel):
    # Optionally categories can be translated too; keep a simple name for now.
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        slug = models.SlugField(
            max_length=255, 
            blank=True, 
            null=True,
            help_text=_("URL-friendly identifier. If left blank, it will be auto-generated from the name."),
            default=None,
            ),
        )
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        for translation in self.translations.all():
            if translation.slug is None or translation.slug == '':
                translation.slug = f"category-{translation.name}"
            translation.save()


class Product(TranslatableModel, BaseModel):
    """Core product model. Translatable fields live in ProductTranslation.

    Keep only language-agnostic fields here (price, category, stock, sku, etc.).
    """
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        description = models.TextField(blank=True),
        # Optional fields: slug, meta_title, meta_description, etc.
        slug = models.SlugField(max_length=255, blank=True, null=True),
        unique_code = models.CharField(
            max_length=4,
            default=get_unique_code(),
            )
    )
    
    sku = models.CharField(max_length=100, blank=True, null=True, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        # Prefer a translated name when possible
        # if self.name:
        #     return self.name
        # return f"Product {self.name} (ID: {self.id})"
        return self.safe_translation_getter('name') or 'Unnamed Product'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        for translation in self.translations.all():
            if translation.slug is None or translation.slug == '':
                translation.slug = f"product-{translation.name}-{translation.unique_code}"
            translation.save()



class ProductImage(BaseModel):
    """
    Multiple images per product.
    Store ordering so admin can control image order. Use an ImageField for uploads.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt = models.CharField(max_length=255, blank=True)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordering', 'id']

    def __str__(self):
        return f"Image {self.pk} for Product {self.product_id}"


class Certificates(BaseModel):
    """Multiple images per product.

    """
    image = models.ImageField(upload_to='certificates/')
    ordering = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Image"
    

class Company(BaseModel,TranslatableModel):
    """Company info model
    """
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        address = models.CharField(max_length=255),
        about_us = models.TextField(),
    )
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    website = models.URLField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return f"Company: {self.translations.name}"
    

class Partners(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="partners", height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return f"Partner: {self.name}"
    

class ServiceBase(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        abstract = True

class Services(ServiceBase):
    PLACES_CHOICES = [
        ('Andijan', 'Andijan'),
        ('Bukhara', 'Bukhara'),
        ('Samarkand', 'Samarkand'),
        ('Tashkent', 'Tashkent'),
        ('Fergana', 'Fergana'),
    ]
    location_url = models.URLField(max_length=2000)
    location = models.CharField(max_length=255,choices=PLACES_CHOICES)

    def __str__(self):
        return f"Service: {self.title}"