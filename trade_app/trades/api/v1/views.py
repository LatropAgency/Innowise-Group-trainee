from django.db import transaction
from django.db.models import Sum, F, Case, When, CharField, IntegerField, DecimalField
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.mixins import (
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.error_serializer import ErrorSerializer
from core.parser import parse
from trades.api.v1.serializers import (
    ItemDetailSerializer,
    WatchListSerializer,
    InventorySerializer,
    ItemsFileSerializer,
    CurrencySerializer,
    ItemListSerializer,
    PriceSerializer,
    OfferSerializer,
    TradeSerializer, ItemIdSerializer, ItemTest,
)
from trades.models import (
    WatchList,
    Inventory,
    Currency,
    Price,
    Offer,
    Trade,
    Item,
)


class CurrencyViewSet(
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ItemViewSet(
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    parser_classes = (MultiPartParser, JSONParser)

    serializer = {
        'list': ItemListSerializer,
    }

    def get_serializer_class(self):
        return self.serializer.get(self.action, ItemDetailSerializer)

    def list(self, request, *args, **kwargs):
        items = self.get_queryset().select_related('currency')
        serializer = ItemListSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], description='Get the most expensive item')
    def expensive(self, *args, **kwargs):
        try:
            item_id = Item.objects.latest('price').id
        except Item.DoesNotExist:
            item_id = None

        response_object = dict(
            expensive=item_id
        )

        return Response(response_object)

    @action(detail=False, methods=['GET'], description='Get the most popular item')
    def popular(self, *args, **kwargs):
        try:
            item_id = Trade.objects.values('item').annotate(sum=Sum('quantity')).latest('sum').get('item', None)
        except Trade.DoesNotExist:
            item_id = None

        response_object = dict(
            popular=item_id
        )

        return Response(response_object)

    @action(detail=False, methods=['GET'], description='Get the most desired item')
    def desired(self, *args, **kwargs):
        try:
            item_id = Offer.objects.values('item').annotate(sum=Sum('quantity')).latest('sum').get('item', None)
        except Offer.DoesNotExist:
            item_id = None

        response_object = dict(
            desired=item_id
        )

        return Response(response_object)

    @action(detail=False, methods=('post',), url_path='statistic')
    def statistic(self, request, *args, **kwargs):
        try:
            expensive_item_id = Item.objects.latest('price').id
        except Item.DoesNotExist:
            expensive_item_id = None
        try:
            popular_item_id = Trade.objects.values('item').annotate(sum=Sum('quantity')).latest('sum').get('item', None)
        except (Trade.DoesNotExist, KeyError):
            popular_item_id = None
        try:
            desired_item_id = Offer.objects.values('item').annotate(sum=Sum('quantity')).latest('sum').get('item', None)
        except Offer.DoesNotExist:
            desired_item_id = None

        response_object = dict(
            popular=popular_item_id,
            expensive=expensive_item_id,
            desired=desired_item_id,
        )

        return Response(response_object)

    @transaction.atomic
    @action(detail=False, methods=('post',), url_path='import')
    def items_import(self, request):
        item_serializer = ItemsFileSerializer(data=request.data)
        item_serializer.is_valid(raise_exception=True)
        errors_list = parse(item_serializer.validated_data['document'])
        error_serializer = ErrorSerializer(data=errors_list, many=True)
        error_serializer.is_valid(raise_exception=True)
        return Response(error_serializer.data)

    @action(detail=False, methods=('post',), url_path='test')
    def test(self, request):
        items_serializer = ItemTest(data=request.data, many=True)
        items_serializer.is_valid(raise_exception=True)
        whens_expressions = []
        for i in items_serializer.validated_data:
            whens_expressions.append(When(id=i['id'], then=i['price']))
        id_list = [item['id'] for item in items_serializer.validated_data]
        items = Item.objects.filter(id__in=id_list).annotate(
            value=Case(
                *whens_expressions,
                output_field=DecimalField(max_digits=7, decimal_places=2),
                default=0.00
            )
        ).annotate(result=F('value') + F('price')).values('id', 'result')

        return Response(items)


class InventoryViewSet(
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class WatchListViewSet(
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    parser_classes = (MultiPartParser, JSONParser)

    @action(detail=True, methods=('post',), url_path='add')
    def add_item_to_watchlist(self, request, pk, *args, **kwargs):
        watch_list = get_object_or_404(WatchList, pk=pk)
        serializer = ItemIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        watch_list.items.add(*serializer.validated_data['items'])
        return Response(status=status.HTTP_201_CREATED)


class PriceViewSet(
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class OfferViewSet(
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    @transaction.atomic
    @action(detail=True, methods=('post',), url_path='buy')
    def buy(self, request, pk, *args, **kwargs):
        serializer = self.get_serializer_class()
        status_code = serializer.buy_offer(request, pk)
        return Response(status=status_code)


class TradeViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
