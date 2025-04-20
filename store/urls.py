from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
# from tutorial.urls import router

# from storefront.urls import urlpatterns
from . import views
from pprint import pprint

# router = SimpleRouter()
# router = DefaultRouter()
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
# pprint(router.urls)

products_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_routers.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_routers = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_routers.register('items', views.CartItemViewSet, basename='cart-items')

#URLConf
urlpatterns = [
    path(r'', include((router.urls))),
    path(r'', include(products_routers.urls)),
    path(r'', include(carts_routers.urls))
]

# urlpatterns = router.urls + product_routers.urls
# urlpatterns = [
#     path('products/' , views.ProductList.as_view()),
#     path('product_detail/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail')
#
# ]