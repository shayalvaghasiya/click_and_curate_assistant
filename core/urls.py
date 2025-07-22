from django.urls import path
from .views import CategoryView, ProductView, Generate_PinContent, PublishPinView

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category-list'),
    path('products/', ProductView.as_view(), name='product-list'),
    path('generate-idea/', Generate_PinContent.as_view(), name='generate-idea'),
    path('publish-pin/', PublishPinView.as_view(), name='publish-pin'),
]
