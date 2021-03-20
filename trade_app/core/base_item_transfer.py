from trades.models import Inventory


class ItemTransfer:
    @classmethod
    def handling_offer(cls, offer, diff):
        offer.price = offer.price / offer.quantity * (offer.quantity - diff)
        offer.quantity = offer.quantity - diff
        if not offer.quantity:
            offer.is_active = False
        offer.save(update_fields=('quantity', 'price', 'is_active'))

    @classmethod
    def get_unit_price(cls, offer):
        return offer.price / offer.quantity

    @classmethod
    def items_transfer(cls, offer, diff, is_buyer=False):
        try:
            inventory_item = Inventory.objects.filter(item=offer.item, user=offer.user).first()
        except Inventory.DoesNotExist:
            inventory_item = Inventory(item=offer.item, user=offer.user, quantity=0)
        inventory_item.quantity = inventory_item.quantity + diff if is_buyer else inventory_item.quantity - diff
        inventory_item.save()
