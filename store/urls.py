from asyncio import base_events
from cgitb import lookup

from django.urls import include, path
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from . import views

# router = SimpleRouter()
router = routers.DefaultRouter()


router.register('products', views.ProductViewset, basename="products")
router.register('collections', views.CollectionViewst),
router.register('carts', views.CartViewset)
router.register('customers', views.CustomerViewset)
router.register('orders', views.OrderViewset, basename="orders")

product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewset,
                        basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewset, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
]
