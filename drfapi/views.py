from drfapi.serailzer import FeedBackSeralizer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# Create your views here.

class FeedBackApi(APIView):
    def post(self, request):
        serializer = FeedBackSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Feedback successfully created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


