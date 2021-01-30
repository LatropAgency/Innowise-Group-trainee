from rest_framework import serializers

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
        fields = ('id', 'user', 'item')


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('id', 'currency', 'item', 'price', 'date')


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'user', 'item', 'entry_quantity', 'quantity', 'order_type', 'price', 'is_active')


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('id', 'item', 'buyer', 'quantity', 'unit_price', 'description', 'buyer_offer', 'seller_offer')
