from celery import shared_task

from core.enum_types import OrderType
from trades.models import (
    Inventory,
    Currency,
    Offer,
    Trade,
    Item,
)


def handling_offer(offer, diff):
    offer.price = offer.price / offer.quantity * (offer.quantity - diff)
    offer.quantity = offer.quantity - diff
    if not offer.quantity:
        offer.is_active = False
    offer.save()


def get_unit_price(offer):
    return offer.price / offer.quantity


def items_transfer(offer, diff, is_buyer=False):
    inventory_item = Inventory.objects.filter(item=offer.item, user=offer.user).first()
    if not inventory_item:
        inventory_item = Inventory(item=offer.item, user=offer.user, quantity=0)
    inventory_item.quantity = inventory_item.quantity + diff if is_buyer else inventory_item.quantity - diff
    inventory_item.save()


@shared_task
def offers_handler():
    items = Item.objects.all()
    offers = Offer.objects.filter(is_active=True)
    for item in items:
        for buy_offer in offers.filter(item=item, order_type=OrderType.BUY.value):
            buy_offer_unit_price = get_unit_price(buy_offer)
            sale_offers = offers.filter(item=item, order_type=OrderType.SALE.value, price__lte=buy_offer.price)
            valid_sale_offers = filter(lambda offer: buy_offer_unit_price >= get_unit_price(offer), sale_offers)
            for sale_offer in sorted(valid_sale_offers, key=lambda offer: get_unit_price(offer)):
                diff = min(buy_offer.quantity, sale_offer.quantity)
                Trade(item=item, seller=sale_offer.user, buyer=buy_offer.user, quantity=diff,
                      unit_price=sale_offer.price / sale_offer.quantity, buyer_offer=buy_offer,
                      seller_offer=sale_offer).save()
                [handling_offer(offer, diff) for offer in [buy_offer, sale_offer]]
                items_transfer(sale_offer, diff)
                items_transfer(buy_offer, diff, True)
                if not buy_offer.quantity:
                    break
