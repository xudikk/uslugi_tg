from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound

from tg.models import Announce
from . import services
from .serializers import AnnounceSerializer


class AnnounceView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AnnounceSerializer

    def get_object(self, *args, **kwargs):
        try:
            product = Announce.objects.get(id=kwargs['id'])
        except Exception as e:
            raise NotFound('not found product')
        return product

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        result = services.one_product(request, root.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        root = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=root, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = services.one_product(request, data.id)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def get(self, request, *args, **kwargs):
        if 'user_id' in kwargs and kwargs['user_id']:
            result = services.get_all_user(request, user_id=kwargs['user_id'])
        elif 'name' in kwargs and kwargs['name']:
            dic = kwargs['name']
            dic = dic.split('_')
            result = services.all_announse(request, int(dic[0]), int(dic[1]), int(dic[2]))
        elif 'id' in kwargs and kwargs['id']:
            result = services.one_product(request, id=kwargs['id'])
        else:
            result = {"item": None}
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        announce = self.get_object(*args, **kwargs)
        announce.is_active = False
        announce.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

