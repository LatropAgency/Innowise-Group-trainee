import csv
import io

from core.item_importer import ItemsImporter
from trades.models import Item


def parse(file):
    error_list = []
    decoded_file = file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    items = ItemsImporter.serialize_objects(csv.reader(io_string, delimiter=','), error_list)
    Item.objects.bulk_create(items, len(items))
    return error_list
