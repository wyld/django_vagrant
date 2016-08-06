from django.shortcuts import render

from rest_framework import serializers, viewsets, permissions

from accounts.models import User


class OnlyCreatorCanModify(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user == obj.creator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'iban', 'creator',)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        OnlyCreatorCanModify)
    queryset = User.objects.all()
    serializer_class = UserSerializer
