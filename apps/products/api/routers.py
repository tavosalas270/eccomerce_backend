# En este apartado defines las rutas de tus viewset
from rest_framework.routers import DefaultRouter
from apps.products.api.views.product_views import ProductViewSet
from apps.products.api.views.general_views import *

router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'measure_unit', MeasureUnitViewSet, basename='measure_unit')
router.register(r'category_products', CategoryProductViewSet, basename='category_products')
router.register(r'indicators', IndicatorViewSet, basename='indicators')

urlpatterns = router.urls