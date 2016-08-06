from django.contrib.auth import get_user_model

from rest_framework import serializers, viewsets, permissions

from accounts.models import User


DjangoUser = get_user_model()


class OnlyCreatorCanModify(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user == obj.creator


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ('id', 'username',)


class UserSerializer(serializers.ModelSerializer):
    creator = OwnerSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'iban', 'creator',)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        OnlyCreatorCanModify)
    queryset = User.objects.all()
    serializer_class = UserSerializer
