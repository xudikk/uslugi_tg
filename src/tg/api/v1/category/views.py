from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound

from tg.models import Category
from . import services
from .serializers import CategorySerializer
from .services import ctg_by_name, deactivate_children


class CategoryView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

    def get_object(self, *args, **kwargs):
        try:
            product = Category.objects.get(slug=kwargs['slug'])
            print("product", product)
        except Exception as e:
            raise NotFound('not found Experience')
        return product

    def get_editserializer_class(self, *args, **kwargs):
        return CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, category=None)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        result = services.get_one_category(request, category.slug)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if 'slug' in kwargs and kwargs['slug']:
            root = self.get_object(*args, **kwargs)
            if "is_active" in request.data and request.data.get("is_active"):
                deactivate_children(root.id, deactivate=False)
            serializer = self.get_serializer(data=request.data, category=root.id, partial=True)
            serializer.is_valid(raise_exception=True)
            category = serializer.save()
            result = services.get_one_category(request, category.slug)
            return Response(result, status=status.HTTP_200_OK)
        else:
            NotFound('not found')

    def get(self, request, *args, **kwargs):
        if 'slug' in kwargs and kwargs['slug']:
            try:
                result = services.get_one_category(request, kwargs['slug'])
                print(kwargs['slug'])
            except:
                result = {"result": "category was deleted"}
        else:
            if request.query_params.get("name"):
                result = ctg_by_name(name=request.query_params.get("name"), parent_id=request.query_params.get("parent_id", None))
            else:
                result = services.get_list_category(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        root = self.get_object(*args, **kwargs)
        root.is_active = False
        deactivate_children(root.id, deactivate=True)
        root.save()
        return Response({"result": f'the item {root} successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
