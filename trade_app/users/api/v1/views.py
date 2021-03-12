from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.state import User

from trades.api.v1.serializers import ItemListSerializer, ItemIdSerializer
from trades.models import WatchList, Item
from users.api.v1.serializers import UserSerializer


class UserViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    """Creates a user instance"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=('get',), url_path='watchlist')
    def get_watchlist(self, request, *args, **kwargs):
        watch_list = WatchList.objects.get(user=request.user).items
        serializer = ItemListSerializer(watch_list, many=True)
        return Response(serializer.data)
