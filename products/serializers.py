from rest_framework import serializers
from .models import Product, ProductCategory, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image','order']

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name','description','order']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False,
        help_text="使用 form-data 上傳圖片，欄位名稱為 uploaded_images"
    )
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id','merchant', 'name', 'description', 'price', 'discount_percent',
            'category','category_name','inventory', 'is_available','sold_count','images', 
            'uploaded_images', 'created_at','updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at','images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)

        # 建立圖片
        for index, image in enumerate(uploaded_images):
            ProductImage.objects.create(product=product, image=image, order=index)

        return product

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 若提供新圖片，則清除舊圖後重建（簡單作法）
        if uploaded_images is not None:
            instance.images.all().delete()
            for index, image in enumerate(uploaded_images):
                ProductImage.objects.create(product=instance, image=image, order=index)

        return instance
    
class CartProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price','images']
        read_only_fields = ['id', 'name', 'price','images']