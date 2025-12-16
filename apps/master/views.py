from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from apps.master.serializers import UserLoginSerializer
from apps.master.models import User

@api_view(['POST'])
def login_user(request):
    print("hi")
    serializer = UserLoginSerializer(data=request.data)

    print(serializer, "-----")

    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username, password=password)

            if not user.is_active:
                return Response({
                    "status": False,
                    "message": "Account is inactive!"
                }, status=status.HTTP_403_FORBIDDEN)

            return Response({
                "status": True,
                "message": "Login Successful",
                "user": {
                    "id": str(user.id),
                    "fullname": user.fullname,
                    "username": user.username,
                    "email": user.email,
                    "mobile": user.mobile,
                }
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "status": False,
                "message": "Invalid username or password!"
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
