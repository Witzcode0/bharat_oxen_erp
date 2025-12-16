from rest_framework import serializers
from apps.products.models import Product, ProductImage, Unit


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "unit",
            "description",
            "specifications",
            "additional_details",
            "images",
            "created_at"
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "unit",
            "description",
            "specifications",
            "additional_details",
            "images"
        ]

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        product = Product.objects.create(**validated_data)

        for img in images:
            ProductImage.objects.create(product=product, image=img)

        return product

class ProductListSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='id', read_only=True)
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'product_id',
            'name',
            'description',
            'first_image'
        ]

    def get_first_image(self, obj):
        image = obj.images.first()
        if image and image.image:
            request = self.context.get('request')
            return request.build_absolute_uri(image.image.url)
        return None
