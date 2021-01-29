from rest_framework import routers

from trades.api.v1.views import (
    WatchListViewSet,
    InventoryViewSet,
    CurrencyViewSet,
    PriceViewSet,
    OfferViewSet,
    TradeViewSet,
    ItemViewSet,
)

router = routers.DefaultRouter()
router.register(r'currencies', CurrencyViewSet)
router.register(r'items', ItemViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'watchlist', WatchListViewSet)
router.register(r'prices', PriceViewSet)
router.register(r'offers', OfferViewSet)
router.register(r'trades', TradeViewSet)

urlpatterns = router.urls
