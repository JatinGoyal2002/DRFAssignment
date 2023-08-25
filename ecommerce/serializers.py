from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        
class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
                'email': {
                    'validators': [
                        UniqueValidator(
                            queryset=User.objects.all()
                        )
                    ]
                }
            }