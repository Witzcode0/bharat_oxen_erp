from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Unit
from .serializers import (
    ProductSerializer, ProductCreateSerializer, UnitSerializer, ProductListSerializer
)
from uuid import UUID
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

# UNIT CRUD
@api_view(["POST"])
def add_unit(request):
    serializer = UnitSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": True, "message": "Unit created", "data": serializer.data})
    return Response({"status": False, "error": serializer.errors})


@api_view(["GET"])
def list_units(request):
    units = Unit.objects.all()
    serializer = UnitSerializer(units, many=True)
    return Response({"status": True, "data": serializer.data})


# PRODUCT CRUD
@api_view(["POST"])
def add_product(request):
    serializer = ProductCreateSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save()
        return Response({"status": True, "message": "Product created", "id": str(product.id)})
    return Response({"status": False, "error": serializer.errors})


@api_view(["GET"])
def list_products(request):
    products = Product.objects.all().order_by("-created_at")
    serializer = ProductSerializer(products, many=True)
    return Response({"status": True, "data": serializer.data})


@api_view(["GET"])
def product_detail(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response({"status": False, "message": "Product not found"}, status=404)

    serializer = ProductSerializer(product)
    return Response({"status": True, "data": serializer.data})


@api_view(["DELETE"])
def delete_product(request, pk):
    try:
        # Validate UUID format first
        UUID(str(pk))
        
        # Then try to delete product
        product = Product.objects.get(id=pk)
        product.delete()
        
        return Response({
            "status": True,
            "message": "Product deleted successfully"
        }, status=status.HTTP_200_OK)

    except ValueError:
        return Response({
            "status": False,
            "message": "Invalid product ID format"
        }, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return Response({
            "status": False,
            "message": "Product not found"
        }, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def product_list_api(request):
    products = Product.objects.prefetch_related('images').all()

    serializer = ProductListSerializer(
        products,
        many=True,
        context={'request': request}
    )

    return Response({
        "status": True,
        "message": "Product list fetched successfully",
        "data": serializer.data
    })