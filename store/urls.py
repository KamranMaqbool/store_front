from asyncio import base_events
from django.urls import include, path
from . import views
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

# router = SimpleRouter()
router = routers.DefaultRouter()


router.register('products', views.ProductViewset, basename="products")
router.register('collections', views.CollectionViewst)

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewset, basename='product-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls))
]
