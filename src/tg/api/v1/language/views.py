from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound

from tg.models import Languages
from . import services
from .serializers import LanguageSerializer



class LanguagesView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LanguageSerializer

    def get_object(self, *args, **kwargs):
        try:
            product = Languages.objects.get(id=kwargs['pk'])
            print("product", product)
        except Exception as e:
            raise NotFound('not found Languages')
        return product

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        result = services.one_lng(request, root.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        root = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=root, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = services.one_lng(request, data.pk)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs['pk']:
            result = services.one_lng(request, kwargs['pk'])
        else:
            result = services.list_lng(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')


    def delete(self, request, *args, **kwargs):
        root = self.get_object(*args, **kwargs)
        root.is_active = False
        root.alias = root.alias + str(root.id)
        root.save()
        return Response(status=status.HTTP_204_NO_CONTENT)