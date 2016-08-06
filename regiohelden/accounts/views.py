from rest_framework import viewsets, permissions

from accounts.models import User
from accounts.permissions import OnlyCreatorCanModify
from accounts.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        OnlyCreatorCanModify)
    queryset = User.objects.all()
    serializer_class = UserSerializer
