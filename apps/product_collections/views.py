from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.cache import cache_response, RedisCacheMixin

from .models import ProductCollection
from .serializers import ProductCollectionSerializer
from .services import CollectionService


@api_view(["GET"])
@cache_response('productcollection')
def get_collections(request):

    collections = CollectionService.get_all_collections()

    serializer = ProductCollectionSerializer(collections, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@cache_response('productcollection')
def get_collection(request, collection_id):

    collection = CollectionService.get_collection(collection_id)

    serializer = ProductCollectionSerializer(collection)

    return Response(serializer.data)


@api_view(["POST"])
@cache_response('productcollection')
def create_collection(request):

    serializer = ProductCollectionSerializer(data=request.data)

    if serializer.is_valid():

        collection = CollectionService.create_collection(serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors)


@api_view(["PUT"])
@cache_response('productcollection')
def update_collection(request, collection_id):

    collection = ProductCollection.objects.get(id=collection_id)

    serializer = ProductCollectionSerializer(collection, data=request.data)

    if serializer.is_valid():

        collection = CollectionService.update_collection(collection, serializer.validated_data)

        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(["DELETE"])
@cache_response('productcollection')
def delete_collection(request, collection_id):

    collection = ProductCollection.objects.get(id=collection_id)

    CollectionService.delete_collection(collection)

    return Response({"message": "Collection deleted"})

from rest_framework import viewsets

class ProductCollectionViewSet(RedisCacheMixin, viewsets.ModelViewSet):
    queryset = ProductCollection.objects.all()
    serializer_class = ProductCollectionSerializer