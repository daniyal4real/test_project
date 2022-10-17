from rest_framework import serializers
from apps.kinopark.models import *



class SeansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seans
        fields = "__all__"
        depth = 1





class MovieSerializer(serializers.ModelSerializer):
    movie_seansy = SeansSerializer(many=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'description',
            'producer',
            'rating',
            'published',
            'image',
            'movie_seansy'
        )



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password"
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
