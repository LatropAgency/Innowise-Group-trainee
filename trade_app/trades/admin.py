from django.contrib import admin
from trades.models import (
    WatchList,
    Inventory,
    Currency,
    Price,
    Offer,
    Trade,
    Item,
)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    ordering = ('code',)
    list_display = ('code', 'name')
    search_fields = ('code',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'price', 'currency')
    search_fields = ('code',)
    ordering = ('code',)
    autocomplete_fields = ('currency',)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity')
    search_fields = ('user',)
    autocomplete_fields = ('user', 'item')
    ordering = ('user__username',)


@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ('user', 'item')
    search_fields = ('user__username',)
    autocomplete_fields = ('user', 'item')
    ordering = ('user__username',)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('item', 'currency', 'price', 'date')
    search_fields = ('item__code',)
    autocomplete_fields = ('item', 'currency')
    ordering = ('item__code',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'entry_quantity', 'quantity', 'order_type', 'price', 'is_active')
    search_fields = ('user__username',)
    autocomplete_fields = ('item', 'user')
    ordering = ('user__username',)


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('item', 'seller', 'buyer', 'quantity', 'unit_price')
    search_fields = ('seller__username', 'buyer__username')
    autocomplete_fields = ('item', 'seller', 'buyer')
    ordering = ('seller__username', 'buyer__username')
