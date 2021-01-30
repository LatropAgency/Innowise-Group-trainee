from rest_framework.mixins import (
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from trades.api.v1.serializers import (
    ItemDetailSerializer,
    WatchListSerializer,
    InventorySerializer,
    CurrencySerializer,
    ItemListSerializer,
    PriceSerializer,
    OfferSerializer,
    TradeSerializer,
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


class CurrencyViewSet(RetrieveModelMixin,
                      DestroyModelMixin,
                      CreateModelMixin,
                      UpdateModelMixin,
                      ListModelMixin,
                      GenericViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ItemViewSet(RetrieveModelMixin,
                  DestroyModelMixin,
                  CreateModelMixin,
                  UpdateModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ItemDetailSerializer
        return super(ItemViewSet, self).retrieve(request, *args, **kwargs)


class InventoryViewSet(RetrieveModelMixin,
                       DestroyModelMixin,
                       CreateModelMixin,
                       UpdateModelMixin,
                       ListModelMixin,
                       GenericViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class WatchListViewSet(RetrieveModelMixin,
                       DestroyModelMixin,
                       CreateModelMixin,
                       UpdateModelMixin,
                       ListModelMixin,
                       GenericViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class PriceViewSet(RetrieveModelMixin,
                   DestroyModelMixin,
                   CreateModelMixin,
                   UpdateModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class OfferViewSet(RetrieveModelMixin,
                   DestroyModelMixin,
                   CreateModelMixin,
                   UpdateModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class TradeViewSet(RetrieveModelMixin,
                   CreateModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
