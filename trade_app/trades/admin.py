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

admin.site.register(Currency)
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(WatchList)
admin.site.register(Price)
admin.site.register(Offer)
admin.site.register(Trade)
