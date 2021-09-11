from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from . import services
from .serializers import RegionSerializer, CategorySerializer
from ...models import Region
from tg.models import Category


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
        elif 'name' in kwargs and kwargs['name']:
            result = services.one_region_by_name(request, kwargs['name'])
        else:
            result = services.list_region(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

    def get_object(self, slug):
        try:
            model = Category.objects.get(slug=slug)
        except Exception as e:
            raise NotFound('not found Region')
        return model

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        result = services.one_category(request, root.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        root = self.get_object(kwargs['slug'])
        serializer = self.get_serializer(data=request.data, instance=root, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = services.one_category(request, data.pk)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def get(self, request, *args, **kwargs):
        if 'slug' in kwargs and kwargs['slug']:
            result = services.one_category_by_name(request, kwargs['slug'])
        else:
            result = services.list_category(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
