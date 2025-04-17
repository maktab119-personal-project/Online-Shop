from rest_framework import serializers
from .models import Product, Category, Discount, Review

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','rating', 'comment', 'review_date']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'level']

class ProductSerializer(serializers.ModelSerializer):
    discounts = DiscountSerializer(many=True, read_only=True)
    review_product = ReviewSerializer(many=True, read_only=True)  # related_name in Review model

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand_name', 'description',
            'img', 'price', 'stock', 'category',
            'discounts', 'review_product',
        ]
