from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from . import services
from .serializers import RegionSerializer
from ...models import Region


class RegionView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegionSerializer

    def get_object(self, pk):
        try:
            model = Region.objects.get(id=pk)
        except Exception as e:
            raise NotFound('not found Region')
        return model

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        result = services.one_region(request, root.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        root = self.get_object(pk)
        serializer = self.get_serializer(data=request.data, instance=root, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = services.one_region(request, data.pk)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs['pk']:
            result = services.one_region(request, kwargs['pk'])
        else:
            result = services.list_region(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)