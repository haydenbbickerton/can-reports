from rest_framework.response import Response
from rest_framework.views import APIView
from .reports import PucsMessageReport


class PucsMessageReportView(APIView):
    """
    A single endpoint for generating a report on PUC messages.
    """
    def get(self, request):
        data = PucsMessageReport().execute() # Returns as a dict
        return Response(data[0])
