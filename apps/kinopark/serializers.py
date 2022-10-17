from rest_framework import serializers
from apps.kinopark.models import *


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
        depth = 1


class CreateOrderSerializer(serializers.ModelSerializer):


    class Meta:
        model = Order
        fields = (
            "price",
            "time",
            "ticket",
            "user"
        )


class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "movie",
            "seans"
        )


class TicketSerializer(serializers.ModelSerializer):
    # ticket_order = OrderSerializer(many=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "movie",
            "seans",
            # "ticket_order"
        )


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class SeansSerializer(serializers.ModelSerializer):
    # seans_seat = SeatSerializer(many=True)

    class Meta:
        model = Seans
        fields = (
            "price",
            "time",
            "language",
            "kinozal_id",
            "movie",
            # "seans_seat"
        )
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


