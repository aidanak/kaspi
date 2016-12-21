from django.shortcuts import render
from rest_framework.views import APIView
from myapp.models import venues,venue_tips
from myapp.serializers import myapp_venuesSerializer
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator

class SearchView(APIView):
    @method_decorator(xframe_options_exempt)
    def get(self, request):
        term = request.GET.get('text')
        addrs = venues.es_search(term)
        myapp_venues_serializer = myapp_venuesSerializer(addrs, many=True)
        response = {}
        response['addrs'] = myapp_venues_serializer.data


        return Response(response)


class IndexView(TemplateView):
    template_name = 'index.html'
