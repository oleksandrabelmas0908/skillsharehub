from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from skillsharehub.mainapp.models import Chanel

import logging

from ..serializers import ChanelOutSerializer, ChanelCreateSerializer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChanelShowViewSet(ModelViewSet):
    queryset = Chanel.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'head', 'options']
    serializer_class = ChanelOutSerializer


class ChanelManageViewSet(ModelViewSet):
    queryset = Chanel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChanelCreateSerializer
    
    def create(self, request):
        # Do not inject owner into incoming data; serializer will set owner
        # from the request context and owner is read-only.
        data = request.data.copy()
        logger.info(f"Creating Chanel with data: {data}")
        serializer = ChanelCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            chanel = serializer.save()
            output_serializer = ChanelOutSerializer(chanel)
            return Response(data=output_serializer.data, status=201)
        return Response(data=serializer.errors, status=400)
    
    def retrieve(self, request, pk=None):
        try:
            chanel = self.get_object()
            serializer = ChanelOutSerializer(chanel)
            return Response(data=serializer.data, status=200)
        except Chanel.DoesNotExist:
            return Response(data={"detail": "Not found."}, status=404)
        
    def update(self, request, pk=None):
        chanel = self.get_object()
        # Pass context so serializer can access request.user; owner is read-only
        serializer = ChanelCreateSerializer(chanel, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            chanel = serializer.save()
            output_serializer = ChanelOutSerializer(chanel)
            return Response(data=output_serializer.data, status=200)
        return Response(data=serializer.errors, status=400)
    
    def partial_update(self, request, pk=None):
        chanel = self.get_object()
        serializer = ChanelCreateSerializer(chanel, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            chanel = serializer.save()
            output_serializer = ChanelOutSerializer(chanel)
            return Response(data=output_serializer.data, status=200)
        return Response(data=serializer.errors, status=400)
    

class ChanelSubscribeViewSet(ModelViewSet):
    queryset = Chanel.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def subscribe(self, request, pk=None):
        try:
            chanel = self.get_object()
            user = request.user
            if user in chanel.subscribers.all():
                return Response(data={"detail": "Already subscribed."}, status=400)
            chanel.subscribers.add(user)
            chanel.save()
            return Response(data={"detail": "Subscribed successfully."}, status=200)
        except Chanel.DoesNotExist:
            return Response(data={"detail": "Not found."}, status=404)
        
    def unsubscribe(self, request, pk=None):
        try:
            chanel = self.get_object()
            user = request.user
            if user not in chanel.subscribers.all():
                return Response(data={"detail": "Not subscribed."}, status=400)
            chanel.subscribers.remove(user)
            chanel.save()
            return Response(data={"detail": "Unsubscribed successfully."}, status=200)
        except Chanel.DoesNotExist:
            return Response(data={"detail": "Not found."}, status=404)