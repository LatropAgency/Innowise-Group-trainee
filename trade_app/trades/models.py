from django.db import models
from rest_framework_simplejwt.state import User

from core.enum_types import OrderType


class StockBase(models.Model):
    """Base"""
    code = models.CharField("Code", max_length=8, unique=True)
    name = models.CharField("Name", max_length=128, unique=True)

    class Meta:
        abstract = True


class Currency(StockBase):
    """Currency"""

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


class Item(StockBase):
    """Particular stock"""
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL, related_name="currency")
    details = models.TextField("Details", blank=True, null=True, max_length=512)


class Inventory(models.Model):
    """The number of stocks a particular user has"""
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="user")
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name="item")
    quantity = models.IntegerField("Stocks quantity", default=0)


class WatchList(models.Model):
    """Current user, favorite list of stocks"""
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="user")
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name="item")


class Price(models.Model):
    """Item prices"""
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL, related_name="currency")
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name="item")
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(unique=True, blank=True, null=True)


class Offer(models.Model):
    """Request to buy or sell specific stocks"""
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="user")
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name="item")
    entry_quantity = models.IntegerField("Requested quantity")
    quantity = models.IntegerField()
    order_type = models.PositiveSmallIntegerField(choices=OrderType.items())
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Trade(models.Model):
    """Information about a certain transaction"""
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name="item")
    seller = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="seller_trade",
        related_query_name="seller_trade",
    )
    buyer = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="buyer_trade",
        related_query_name="buyer_trade",
    )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    buyer_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="buyer_offer",
        related_query_name="buyer_offer",
    )
    seller_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="seller_offer",
        related_query_name="seller_offer",
    )
