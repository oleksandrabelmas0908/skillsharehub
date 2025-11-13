from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView, 
    ChanelShowViewSet, ChanelManageViewSet, ChanelSubscribeViewSet, 
    PostChanelViewSet, PostManageViewSet,
    CommentPostViewSet, CommentManageViewSet,
)

router = routers.DefaultRouter()
urlpatterns = [
    path('auth/', RegisterView.as_view(), name='register'),

    path('chanels/', ChanelShowViewSet.as_view({'get': 'list'}), name='chanel_show'),
    path('chanels/manage/', ChanelManageViewSet.as_view({'post': 'create'}), name='chanel_manage_create'),
    path('chanels/manage/<int:pk>/', ChanelManageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='chanel_manage_detail'),
    path('chanels/subscribe/<int:pk>/', ChanelSubscribeViewSet.as_view({'post': 'subscribe'}), name='subscribe_chanel'),
    path('chanels/unsubscribe/<int:pk>/', ChanelSubscribeViewSet.as_view({'post': 'unsubscribe'}), name='unsubscribe_chanel'),

    path('posts/', PostChanelViewSet.as_view({'get': 'list'}), name='chanel_post_list'),
    path('posts/<int:pk>/', PostChanelViewSet.as_view({'get': 'retrieve'}), name='post_detail'),
    path('posts/manage/', PostManageViewSet.as_view({'post': 'create'}), name='post_manage'),
    path('posts/manage/<int:pk>/', PostManageViewSet.as_view({
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='post_manage_detail'),

    path('comments/<int:post_pk>/', CommentPostViewSet.as_view({'get': 'list'}), name='comment_post_list'),
    path('comments/manage/<int:post_pk>/', CommentManageViewSet.as_view({'post': 'create'}), name='comment_manage_list'),
    path('comments/manage/delete/<int:pk>/', CommentManageViewSet.as_view({'delete': 'destroy'}), name='comment_manage_detail'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
