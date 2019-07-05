from rest_framework import serializers
from .models import Movie

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id','name','type','country','length','release_time','score','score_num','box_office')

class Movie2Serializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id','name','type','country','length','release_time','score','score_num','box_office')