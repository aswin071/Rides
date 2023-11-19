from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ride
from .serializers import RideSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RideCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = RideSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Ride created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RideDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, ride_id):
        try:
            ride = Ride.objects.get(pk=ride_id)
            serializer = RideSerializer(ride)
            return Response(serializer.data)
        except Ride.DoesNotExist:
            return Response({"message": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)


class RideListView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            rides = Ride.objects.all()
            serializer = RideSerializer(rides, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)