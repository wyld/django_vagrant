from django.contrib.auth import get_user_model

from rest_framework import serializers

from accounts.models import User


DjangoUser = get_user_model()


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ('id', 'username',)


class UserSerializer(serializers.ModelSerializer):
    creator = OwnerSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'iban', 'creator',)
