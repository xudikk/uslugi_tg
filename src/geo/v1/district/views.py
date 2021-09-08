from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from . import services
from .serializers import DistrictSerializer
from ...models import District


class DistrictView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DistrictSerializer

    def get_object(self, pk):
        try:
            model = District.objects.get(id=pk)
        except Exception as e:
            raise NotFound('not found District')
        return model

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        result = services.one_model(request, root.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        root = self.get_object(pk)
        serializer = self.get_serializer(data=request.data, instance=root, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = services.one_model(request, data.pk)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs['pk']:
            result = services.one_model(request, kwargs['pk'])
        else:
            result = services.list_model(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)