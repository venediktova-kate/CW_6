from django.shortcuts import get_object_or_404
from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from ads.models import Ad, Comment
from ads.permissions import IsOwner, IsAdmin
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    default_serializer = AdSerializer
    serializers = {
        "list": AdSerializer,
        "retrieve": AdDetailSerializer,
        "create": AdDetailSerializer,
        "update": AdDetailSerializer,
        "partial_update": AdDetailSerializer,
        "destroy": AdDetailSerializer
    }
    permissions = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner | IsAdmin],
        "partial_update": [IsAuthenticated, IsOwner | IsAdmin],
        "destroy": [IsAuthenticated, IsOwner | IsAdmin]
    }
    default_permission = [AllowAny]
    pagination_class = AdPagination

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def get_queryset(self):
        if self.action == 'me':
            return Ad.objects.filter(author=self.request.user).all()
        return Ad.objects.all()

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permissions = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner | IsAdmin],
        "partial_update": [IsAuthenticated, IsOwner | IsAdmin],
        "destroy": [IsAuthenticated, IsOwner | IsAdmin]
    }
    default_permission = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(ad=self.kwargs['ad_pk'])

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def perform_create(self, serializer):
        user = self.request.user
        ad_id = self.kwargs.get('ad_pk')
        ad_instance = get_object_or_404(Ad, id=ad_id)
        serializer.save(author=user, ad=ad_instance)
