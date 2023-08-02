from rest_framework import viewsets, mixins
from django.contrib.auth import get_user_model
from .pagination import PageNumberPaginationWithLimit
from .serializers import TransactionSerializers, UserSerializer


class ListUpdateViewSet(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    pass


class TransactionViewSet(ListUpdateViewSet):
    """Transaction view set"""
    queryset = get_user_model().objects.all()
    pagination_class = PageNumberPaginationWithLimit
    http_method_names = ['get', 'patch']

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            return UserSerializer(*args, **kwargs)
        if self.request.method == 'PATCH':
            return TransactionSerializers(*args, **kwargs)

    @transaction.atomic
    def perform_update(self, serializer):
        sender = self.get_object()
        validated_data = serializer.validated_data
        receivers = User.objects.filter(
            tax_id_number__in=validated_data['receivers'])
        perform_transactions(sender, receivers, validated_data)
        super().perform_update(serializer)
