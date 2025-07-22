from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from decouple import config
import google.generativeai as genai
from .models import Category
from .serializers import CategorySerializer, ProductSerializer
from .scrapper import bestseller_scrapper
from django.shortcuts import get_object_or_404

try:
    genai.configure(api_key=config("GOOGLE_API_KEY"))
except Exception as e:
    print(f"Could not configure API KEY: {e}")

def generate_affiliate_link(asin, associate_tag="shayalvaghasi-21"):
    """Generate a simple amazon affiliate link"""
    return f"https://www.amazon.in/dp/{asin}/?tag={associate_tag}"

def generate_AI_content(product_title, category_name):
    """Call GEMINI API to generate a Pin title and description
    Return a dictionary with title and description"""

    try: 
        model = genai.GenerativeModel("gemini-pro")
        prompt = (
            f"You are a Pinterest marketing expert creating content for an affiliate marketing board. "
            f"Given the following product information, generate an engaging Pin Title and a Pin Description.\n\n"
            f"Product Title: {product_title}\n"
            f"Product Category: {category_name}\n\n"
            f"Instructions:\n"
            f"- The Pin Title should be catchy and enticing, around 50-70 characters.\n"
            f"- The Pin Description should be enthusiastic and around 200-300 characters. "
            f"It should highlight the product's appeal for its category and include a call to action. "
            f"Include 3-4 relevant hashtags like #AmazonFinds, #HomeDecor, etc.\n\n"
            f"Please return ONLY the generated text, with the title and description separated by a '|||' delimiter. "
            f"Example: My Awesome Title ||| This is the amazing description for the product! #tag1 #tag2"
        )

        response = model.generate_content(prompt)
        parts = response.text.strip().split("|||")

        if len(parts) == 2:
            return {
                'pin_title' : parts[0].strip(),
                'pin_description' : parts[1].strip()
            }
        else:
           return {
                'pin_title': f"✨ Must-Have Find: {product_title} ✨",
                'pin_description': response.text.strip()
            } 

    except Exception as e:
        print(f"Error during AI content generation: {e}")
        return {
            'pin_title': f"✨ Check out this {product_title}! ✨",
            'pin_description': f"A fantastic find for your {category_name} collection. Discover more on Amazon! #AmazonFinds"
        }

class CategoryView(generics.ListAPIView):
    """
    An API to list all categories
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer

class ProductView(APIView):
    """
    An API view to scrap products based on a category from amazon bestseller page.
    and return them directly without saving in database.
    """

    def get(self, request, *args, **kwargs):

        category_id = request.query_params.get('category')
        if not category_id:
            return Response({"error": "Category id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        category = get_object_or_404(Category, id=category_id)

        try:
            print(f"Starting scrape for category: '{category.name}'...")
            scrapped_products = bestseller_scrapper(category.urls)

            serializer = ProductSerializer(scrapped_products, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            print(f"An error occured during scrapping:{e}")
            return Response({"error":"An internal error occured while scrapping."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class Generate_PinContent(APIView):
    """Receive data from selected product, AI content generation for pin and 
    return a complete pin idea with title, description, link, images etc..."""

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        product_data = serializer.validated_data
        category = product_data['category']

        # simulate AI content generation
        ai_content = generate_AI_content(product_data['title'], category.name)

        affiliate_link = generate_affiliate_link(product_data['asin'])

        pin_idea = {
            'product' : product_data,
            'pin_title' : ai_content['pin_title'],
            'pin_description' : ai_content['pin_description'],
            'affiliate_link' : affiliate_link
        }

        return Response(pin_idea, status=status.HTTP_200_OK)
