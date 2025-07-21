from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryView(generics.ListAPIView):
    """
    An API to list all categories
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer

class ProductView(generics.ListAPIView):
    """
    An API view to list products based on a category.
    Filters products based on the 'category' query parameter.
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        This method is overridden to filter products based on the
        'category' ID provided in the URL query parameters.
        """
        
        category_id = self.request.query_params.get('category')

        if category_id:
            # API call to get products based on category

            products = Product.objects.filter(category_id=category_id)

            if not products.exists():
                print(f"No more products for category {category_id}. Creating now...")
                self.create

