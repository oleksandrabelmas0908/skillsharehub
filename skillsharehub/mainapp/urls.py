from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, ChanelShowViewSet, ChanelManageViewSet, ChanelSubscribeViewSet


router = routers.DefaultRouter()
urlpatterns = [
    path('auth/', RegisterView.as_view(), name='register'),

    path('chanels/', ChanelShowViewSet.as_view({'get': 'list'}), name='chanel_show'),
    path('chanels/manage/', ChanelManageViewSet.as_view({'post': 'create'}), name='chanel_manage_list'),
    path('chanels/manage/<int:pk>/', ChanelManageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='chanel_manage_detail'),
    path('chanels/subscribe/<int:pk>/', ChanelSubscribeViewSet.as_view({'post': 'subscribe'}), name='subscribe_chanel'),
    path('chanels/unsubscribe/<int:pk>/', ChanelSubscribeViewSet.as_view({'post': 'unsubscribe'}), name='unsubscribe_chanel'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
