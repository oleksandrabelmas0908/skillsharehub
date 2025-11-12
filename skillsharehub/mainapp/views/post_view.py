from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

import logging

from skillsharehub.mainapp.models import Post
from skillsharehub.mainapp.serializers import PostOutSerializer, PostDetailSerializer, PostCreateSerializer, PostUpdateSerializer
from skillsharehub.mainapp.filters import PostFilter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostChanelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PostOutSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']  

    def get_queryset(self):
        """
        Optionally filter posts by chanel_pk if provided in URL kwargs.
        Otherwise return all posts with filters applied.
        """
        queryset = super().get_queryset()
        chanel_pk = self.kwargs.get('chanel_pk')
        if chanel_pk is not None:
            queryset = queryset.filter(chanel__pk=chanel_pk)
        return queryset
    
    def retrieve(self, request, pk=None):
        post = self.get_object()
        serializer = PostDetailSerializer(post)
        return Response(data=serializer.data, status=200)
        

class PostManageViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            chanel = serializer.validated_data.get('chanel')
            if chanel is None:
                logger.warning("Chanel field is missing in the request data.")
                return Response(data={"chanel": "This field is required."}, status=400)
            if chanel.owner != request.user:
                logger.warning(f"User {request.user} attempted to create a post for chanel {chanel} they do not own.")
                return Response(data={"detail": "You do not own this chanel."}, status=403)

            post = serializer.save()
            output_serializer = PostDetailSerializer(post)
            return Response(data=output_serializer.data, status=201)
        
        logger.warning(f"Post creation failed with errors: {serializer.errors}")
        return Response(data=serializer.errors, status=400)
    
    def update(self, request, pk=None):
        post = self.get_object()
        chanel = post.chanel
        if chanel.owner != request.user:
            logger.warning(f"User {request.user} attempted to update a post for chanel {chanel} they do not own.")
            return Response(data={"detail": "You do not own this chanel."}, status=403)

        serializer = PostUpdateSerializer(post, data=request.data, partial=False)
        if serializer.is_valid():
            post = serializer.save()
            output_serializer = PostDetailSerializer(post)
            logger.info(f"Post with pk={post.pk} updated by user {request.user}.")
            return Response(data=output_serializer.data, status=200)
        logger.warning(f"Post update failed with errors: {serializer.errors}")
        return Response(data=serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        post = self.get_object()
        chanel = post.chanel
        if chanel.owner != request.user:
            logger.warning(f"User {request.user} attempted to partially update a post for chanel {chanel} they do not own.")
            return Response(data={"detail": "You do not own this chanel."}, status=403)

        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            post = serializer.save()
            output_serializer = PostDetailSerializer(post)
            logger.info(f"Post with pk={post.pk} partially updated by user {request.user}.")
            return Response(data=output_serializer.data, status=200)
        logger.warning(f"Post partial update failed with errors: {serializer.errors}")
        return Response(data=serializer.errors, status=400)
    
    def destroy(self, request, pk=None):
        post = self.get_object()
        chanel = post.chanel
        if chanel.owner != request.user:
            logger.warning(f"User {request.user} attempted to delete a post for chanel {chanel} they do not own.")
            return Response(data={"detail": "You do not own this chanel."}, status=403)

        post.delete()
        logger.info(f"Post with pk={pk} deleted by user {request.user}.")
        return Response(status=204)