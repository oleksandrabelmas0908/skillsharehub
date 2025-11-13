from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

import logging

from skillsharehub.mainapp.serializers import CommentOutSerializer, CommentCreateSerializer
from skillsharehub.mainapp.models import Comment, Post


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommentPostViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CommentOutSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def list(self, request, post_pk=None):
        comments = self.queryset.filter(post=post_pk)
        serializer = self.serializer_class(comments, many=True)
        logger.info(f"Listing comments for post {post_pk}, found {comments.count()} comments.")
        return Response(data=serializer.data, status=200)
    

class CommentManageViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer
    http_method_names = ['post', 'put', 'delete', 'head', 'options']

    def create(self, request, post_pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            post = Post.objects.filter(pk=post_pk).first()
            if post is None:
                logger.warning(f"Post with ID {post_pk} does not exist.")
                return Response(data={"post": "Post does not exist."}, status=400)
            
            comment = serializer.save(author=request.user, post=post)
            output_serializer = CommentOutSerializer(comment)
            logger.info(f"Created comment with ID {comment.id}.")
            return Response(data=output_serializer.data, status=201)
        logger.error(f"Failed to create comment: {serializer.errors}")
        return Response(data=serializer.errors, status=400)
    
    def destroy(self, request, pk=None):
        try:
            comment = self.get_object()
            if comment.author != request.user:
                logger.warning(f"User {request.user} attempted to delete comment {pk} they do not own.")
                return Response(data={"detail": "You do not own this comment."}, status=403)
            comment.delete()
            logger.info(f"Deleted comment with ID {pk}.")
            return Response(status=204)
        except Comment.DoesNotExist:
            logger.error(f"Comment with ID {pk} does not exist.")
            return Response(data={"detail": "Not found."}, status=404)