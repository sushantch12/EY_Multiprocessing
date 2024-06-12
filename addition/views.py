from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdditionRequestSerializer, AdditionResponseSerializer
from .controllers import perform_addition
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)


class AddNumbersView(APIView):
    def post(self, request):
        serializer = AdditionRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                started_at = datetime.now()
                logging.info(f"Starting addition process for batchid: {serializer.validated_data['batchid']}")

                response = perform_addition(serializer.validated_data['payload'])

                completed_at = datetime.now()
                logging.info(f"Completed addition process for batchid: {serializer.validated_data['batchid']}")

                response_data = {
                    "batchid": serializer.validated_data['batchid'],
                    "response": response,
                    "status": "complete",
                    "started_at": started_at.isoformat(),
                    "completed_at": completed_at.isoformat()
                }

                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                logging.error(f"Error processing batchid: {serializer.validated_data['batchid']} - {str(e)}")
                return Response({"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logging.warning(f"Invalid request data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
