from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dog_app.serializers import DogSerializer, BreedSerializer
from dog_app.models import Dog, Breed


class AbstractList(APIView):
    model = None
    serializer = None

    def get(self, request):
        queryset = self.model.objects.all()
        serializer = self.serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AbstractDetail(APIView):
    model = None
    serializer = None

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = self.serializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DogList(AbstractList):
    model = Dog
    serializer = DogSerializer


class DogDetail(AbstractDetail):
    model = Dog
    serializer = DogSerializer


class BreedList(AbstractList):
    model = Breed
    serializer = BreedSerializer


class BreedDetail(AbstractDetail):
    model = Breed
    serializer = BreedSerializer
