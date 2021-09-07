from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound

from tg.models import Log
from . import services
from .serializers import UserLogSerializer


class UserLogView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLogSerializer

    def get_object(self, *args, **kwargs):
        try:
            product = Log.objects.get(user_id=kwargs['user_id'])
        except Exception as e:
            raise NotFound('not found product')
        return product

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        result = services.one_product(request, root.user_id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        root = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=root, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = services.one_product(request, data.user_id)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def get(self, request, *args, **kwargs):
        if 'user_id' in kwargs and kwargs['user_id']:
            result = services.one_product(request, tg_id=kwargs['user_id'])
        else:
            result = {"item": None}
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')
