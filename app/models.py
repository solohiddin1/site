from django.db import models
from django.core.exceptions import ObjectDoesNotExist


# Simple language table. Admin can add languages (e.g. 'uz', 'ru', 'en').
# One language can be marked as default (we'll use that as fallback).
class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)  # e.g. 'uz', 'ru', 'en'
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "language"
        verbose_name_plural = "languages"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Category(models.Model):
    # Optionally categories can be translated too; keep a simple name for now.
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class CategoryTranslation(models.Model):
    """
    Translatable fields for Category.
    Each category can have multiple CategoryTranslation rows, one per language.
    """
    category = models.ForeignKey(Category, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = (('category', 'language'),)

    def __str__(self):
        return f"{self.category_id} - {self.language.code}: {self.name}"

class Product(models.Model):
    """Core product model. Translatable fields live in ProductTranslation.

    Keep only language-agnostic fields here (price, category, stock, sku, etc.).
    """
    sku = models.CharField(max_length=100, blank=True, null=True, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Prefer a translated name when possible
        t = self.get_translation()
        if t and t.name:
            return t.name
        return self.sku or f"Product {self.pk}"

    def get_default_language(self):
        """Return default Language instance. If none configured, fall back to code 'uz' or None."""
        try:
            default = Language.objects.filter(is_default=True).first()
            if default:
                return default
            # fallback to 'uz' by code
            return Language.objects.filter(code__iexact='uz').first()
        except Exception:
            return None

    def get_translation(self, lang_code: str | None = None):
        """Return a ProductTranslation for lang_code, with fallback to default language then any translation.

        Usage: product.get_translation('ru') or product.get_translation() will use request language or default.
        """
        qs = self.translations.select_related('language')
        if lang_code:
            try:
                return qs.get(language__code__iexact=lang_code)
            except ObjectDoesNotExist:
                pass

        # try default language
        default = self.get_default_language()
        if default:
            try:
                return qs.get(language=default)
            except ObjectDoesNotExist:
                pass

        # fallback to any available translation
        return qs.first()

    def translated_field(self, field_name: str, lang_code: str | None = None):
        """Convenience to fetch a translated field value with fallback.

        Example: product.translated_field('name', 'ru')
        """
        t = self.get_translation(lang_code=lang_code)
        if not t:
            return None
        return getattr(t, field_name, None)

    @property
    def name(self):
        return self.translated_field('name')

    @property
    def description(self):
        return self.translated_field('description')


class ProductTranslation(models.Model):
    """Translatable fields for Product.

    Each product can have multiple ProductTranslation rows, one per language.
    """
    product = models.ForeignKey(Product, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Optional fields: slug, meta_title, meta_description, etc.
    slug = models.SlugField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = (('product', 'language'),)

    def __str__(self):
        return f"{self.product_id} - {self.language.code}: {self.name}"


class ProductImage(models.Model):
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


class Certificates(models.Model):
    """Multiple images per product.

    """
    image = models.ImageField(upload_to='certificates/')
    ordering = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Image"
    

class Company(models.Model):
    """Company info model
    """
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    about_us = models.TextField()

    def __str__(self):
        return f"Company: {self.name}"
    

class Partners(models.Model):
    name = models.CharField()
    image = models.ImageField( upload_to="partners", height_field=None, width_field=None, max_length=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

    def __str__(self):
        return f"Partner: {self.name}"
    

class ServiceBase(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

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
    title = models.CharField(max_length=255)
    location_url = models.URLField(max_length=2000)
    location = models.CharField(max_length=255,choices=PLACES_CHOICES)

    def __str__(self):
        return f"Service: {self.title}"