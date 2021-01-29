from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.state import User

from users.api.v1.serializers import UserSerializer


class UserViewSet(CreateModelMixin, GenericViewSet):
    """Creates a user instance"""
    permission_classes = (~IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
