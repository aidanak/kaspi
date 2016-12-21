from rest_framework import serializers
from myapp.models import venues
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from django.contrib.gis.geos import Point


class myapp_venuesSerializer(GeoFeatureModelSerializer):

    point = GeometrySerializerMethodField()

    def get_point(self, obj):
        return Point(obj.lat, obj.lon)

    class Meta:
        model = venues
        geo_field = "point"
        fields = ('name')


