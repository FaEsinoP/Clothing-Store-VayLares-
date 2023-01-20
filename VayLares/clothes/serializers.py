from rest_framework import serializers
from .models import *


class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('__all__')
