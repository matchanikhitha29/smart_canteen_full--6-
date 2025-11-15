from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Item, Order
from .serializers import ItemSerializer, OrderSerializer


# ---------------------------
# API: ITEMS LIST
# ---------------------------
@api_view(['GET'])
def items_list(request):
    try:
        items = Item.objects.filter(available=True)
        serializer = ItemSerializer(items, many=True)

        return Response(
            {
                "status": "success",
                "count": items.count(),
                "items": serializer.data
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {
                "status": "error",
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ---------------------------
# API: ORDERS LIST
# ---------------------------
@api_view(['GET'])
def orders_list(request):
    try:
        # Ensure created_at exists
        if not hasattr(Order, "created_at"):
            return Response(
                {
                    "status": "error",
                    "message": "Order model missing 'created_at'. Add it to models."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        orders = Order.objects.all().order_by('-created_at')[:20]
        serializer = OrderSerializer(orders, many=True)

        return Response(
            {
                "status": "success",
                "count": orders.count(),
                "orders": serializer.data
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {
                "status": "error",
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
