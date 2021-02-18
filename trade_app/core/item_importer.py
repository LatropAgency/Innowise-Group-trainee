from trades.models import Item


class ItemsImporter:
    @staticmethod
    def value_to_int(value):
        return int(value)

    @staticmethod
    def serialize_objects(csv_items, error_list):
        item_list = []
        for code, name, price, currency, details in csv_items:
            item_list.append(Item(code=code, name=name, price=ItemsImporter.value_to_int(price),
                                  currency_id=ItemsImporter.value_to_int(currency), details=details))
            if ItemsImporter.value_to_int(price) > 200:
                error_list.append({'message': f'Item({code}) is to expensive'})
        return item_list
