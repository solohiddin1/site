from django.db import transaction
from rest_framework import serializers

from .models import (
	Language,
	Category,
	Product,
	ProductTranslation,
	ProductImage,
)


class LanguageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Language
		fields = ['id', 'name', 'code', 'is_default']


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'name']


class ProductTranslationSerializer(serializers.ModelSerializer):
	# use language code to identify language in nested payloads
	language = serializers.SlugRelatedField(slug_field='code', queryset=Language.objects.all())

	class Meta:
		model = ProductTranslation
		fields = ['id', 'language', 'name', 'description', 'slug']


class ProductImageSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	image = serializers.ImageField(required=False)

	class Meta:
		model = ProductImage
		fields = ['id', 'image', 'alt', 'ordering']


class ProductSerializer(serializers.ModelSerializer):
	translations = ProductTranslationSerializer(many=True, required=False)
	images = ProductImageSerializer(many=True, required=False)
	category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

	# expose read-only resolved fields for convenience
	name = serializers.CharField(read_only=True)
	description = serializers.CharField(read_only=True)

	class Meta:
		model = Product
		fields = [
			'id', 'sku', 'price', 'category', 'created_at', 'updated_at',
			'translations', 'images', 'name', 'description',
		]
		read_only_fields = ['created_at', 'updated_at', 'name', 'description']

	def _create_or_update_translations(self, product, translations_data):
		"""Create or update ProductTranslation rows for the product."""
		for t in translations_data:
			lang = t.pop('language')
			ProductTranslation.objects.update_or_create(
				product=product, language=lang, defaults=t
			)

	def _replace_images(self, product, images_data):
		"""Simple behavior: delete existing images and recreate in provided order.

		This keeps implementation straightforward for typical admin submissions.
		"""
		# remove old images
		product.images.all().delete()
		objs = []
		for img in images_data:
			image_file = img.get('image', None)
			alt = img.get('alt', '')
			ordering = img.get('ordering', 0)
			objs.append(ProductImage(product=product, image=image_file, alt=alt, ordering=ordering))
		if objs:
			ProductImage.objects.bulk_create(objs)

	@transaction.atomic
	def create(self, validated_data):
		translations_data = validated_data.pop('translations', [])
		images_data = validated_data.pop('images', [])

		product = Product.objects.create(**validated_data)

		if translations_data:
			self._create_or_update_translations(product, translations_data)

		if images_data:
			self._replace_images(product, images_data)

		return product

	@transaction.atomic
	def update(self, instance, validated_data):
		translations_data = validated_data.pop('translations', None)
		images_data = validated_data.pop('images', None)

		# update simple fields
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()

		if translations_data is not None:
			self._create_or_update_translations(instance, translations_data)

		if images_data is not None:
			# replace existing images with provided list
			self._replace_images(instance, images_data)

		return instance

