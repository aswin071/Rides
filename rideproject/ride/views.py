from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ride,Driver
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


class RideStatusUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, ride_id):
        try:
            ride = Ride.objects.get(pk=ride_id)
            new_status = request.data.get('status')

            if new_status not in ['started', 'completed', 'cancelled']:
                return Response({"message": "Invalid status provided"}, status=status.HTTP_400_BAD_REQUEST)

            ride.status = new_status
            ride.save()

            serializer = RideSerializer(ride)
            return Response(serializer.data)
        except Ride.DoesNotExist:
            return Response({"message": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)


class DriverRideAcceptView(APIView):
    def put(self, request, ride_id):
        try:

            driver_id = request.user.id 
            ride = Ride.objects.get(pk=ride_id)
            driver_request = DriverRideRequest.objects.filter(driver_id=driver_id, ride_id=ride_id).first()
            
            if driver_request:
                driver_request.accepted = True
                driver_request.save()
                ride.driver_accepted = True
                ride.save()
                return Response({"message": "Ride request accepted"})
            else:
                return Response({"message": "No ride request found"}, status=status.HTTP_404_NOT_FOUND)
        except Ride.DoesNotExist:
            return Response({"message": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)