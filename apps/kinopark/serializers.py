from rest_framework import serializers
from apps.kinopark.models import *


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'description',
            'producer',
            'rating',
            'published'
        )


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorization
        fields = "__all__"
