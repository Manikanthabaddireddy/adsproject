from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from WebApp.models import Finance_Model,Web_Model,Remainder_Model


class Ser(serializers.ModelSerializer):
    class Meta:
        model=Finance_Model
        fields='__all__'

    class Meta:
        model=Web_Model
        fields='__all__'

    class Meta:
        model=Remainder_Model
        fields='__all__'