from django.forms import model_to_dict
from django.shortcuts import render

from .serializers import WomenSerializer
from .models import Women
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

class WomenAPIView(APIView):
    def get(self, request):
        lst = Women.objects.all().values()
        return Response({'posts': WomenSerializer(lst, many=True).data})
    
    def post(self, request):
        serializer = WomenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})
    
    def create(self, validated_data):
        return Women.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content')
        instance.time_update = validated_data.get('time_update')
        instance.is_published = validated_data.get('is_published')
        instance.cat_id = validated_data.get('cat_id')
        instance.save()
        return instance
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'no key'})
        
        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({'error': 'that was a miistake'})
        
        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exceptions=True)
        serializer.save()

# class WomenAPIView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

