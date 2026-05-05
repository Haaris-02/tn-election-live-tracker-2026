from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Constituency
from .serializers import ConstituencySerializer

@api_view(['GET'])
def get_constituencies(request):
    constituencies = Constituency.objects.all()
    serializer = ConstituencySerializer(constituencies, many=True)
    return Response(serializer.data)