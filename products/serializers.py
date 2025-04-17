from rest_framework import serializers
from .models import Product, Category, Discount, Review

class DiscountCreateSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Discount
        fields = [
            'id', 'code', 'value', 'is_percentage',
            'start_date', 'end_date', 'product_ids'
        ]

    def create(self, validated_data):
        product_ids = validated_data.pop('product_ids', [])
        discount = Discount.objects.create(**validated_data)
        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                product.discounts.add(discount)
        return discount



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','rating', 'comment', 'review_date']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'level']

class ProductSerializer(serializers.ModelSerializer):
    discounts = DiscountCreateSerializer(many=True, read_only=True)
    review_product = ReviewSerializer(many=True, read_only=True)  # related_name in Review model
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand_name', 'description',
            'img', 'price', 'stock', 'category',
            'discounts', 'review_product', 'discount_price',
        ]

    def get_discount_price(self, obj):
        return obj.get_discount_price()
