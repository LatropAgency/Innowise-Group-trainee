from django.shortcuts import get_object_or_404
from rest_framework import serializers, status

from core.base_item_transfer import ItemTransfer
from core.enum_types import OrderType
from trades.models import (
    WatchList,
    Inventory,
    Currency,
    Price,
    Offer,
    Trade,
    Item,
)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'code', 'name')


class ItemListSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=False)

    class Meta:
        model = Item
        fields = ('id', 'code', 'name', 'price', 'currency')


class ItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'code', 'name', 'price', 'currency', 'details')


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'user', 'item', 'quantity')


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ('id', 'user', 'items')


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('id', 'currency', 'item', 'price', 'date')


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'user', 'item', 'entry_quantity', 'quantity', 'order_type', 'price', 'is_active')

    @staticmethod
    def buy_offer(request, pk):
        sale_offer = get_object_or_404(Offer, id=pk)
        buy_offer = Offer(user=request.user, quantity=sale_offer.quantity, entry_quantity=sale_offer.quantity,
                          price=sale_offer.price, order_type=OrderType.BUY.value, item=sale_offer.item)
        buy_offer.save()
        diff = min(buy_offer.quantity, sale_offer.quantity)
        Trade(item=sale_offer.item, seller=sale_offer.user, buyer=buy_offer.user, quantity=diff,
              unit_price=sale_offer.price / sale_offer.quantity, buyer_offer=buy_offer,
              seller_offer=sale_offer).save()
        [ItemTransfer.handling_offer(offer, diff) for offer in [buy_offer, sale_offer]]
        ItemTransfer.items_transfer(sale_offer, diff)
        ItemTransfer.items_transfer(buy_offer, diff, True)


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('id', 'item', 'buyer', 'quantity', 'unit_price', 'description', 'buyer_offer', 'seller_offer')


class ItemsFileSerializer(serializers.Serializer):
    document = serializers.FileField()

    class Meta:
        fields = ('document',)


class ItemIdSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        fields = ('items',)


class ItemTest(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()

    class Meta:
        fields = ('id', 'price',)
