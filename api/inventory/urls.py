from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductView.as_view()),
    path('products/<int:id>/', views.ProductView.as_view()),
    path('products/model/',
         views.ProductModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('purchases/', views.PurchaseView.as_view()),
    path('sales/', views.SaleView.as_view()),
    path('inventories/<int:id>/', views.InventoryView.as_view()),

    path('sync/', views.SalesSyncView.as_view()),
]
