from django.urls import include, path
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter

# router = SimpleRouter()
router = DefaultRouter()

router.register('products', views.ProductViewset)
router.register('collections', views.CollectionViewst)


urlpatterns = [
    path('', include(router.urls))
]
