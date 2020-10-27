from rest_framework import serializers 
from cars.models import Car,Rate,Maker
from django.db.models import Avg


class MakerSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Maker
        fields = ('Make_ID',
                  'Make_Name')

class CarsSerializer(serializers.ModelSerializer):

    Make_Name = serializers.SerializerMethodField('get_Make_Name')
    Make_ID = serializers.SerializerMethodField('get_Make_ID')
    Rates = serializers.SerializerMethodField('get_Rates')

    def get_Make_ID(self, Car):
        if hasattr(Car, "__getitem__"):
            pk_value = Car['Maker'].pk
            maker_inst = Maker.objects.get(pk=pk_value)
            return maker_inst.Make_ID
        else:
            return Car.Maker.Make_ID
        return None
        
    def get_Make_Name(self, Car):
        if hasattr(Car, "__getitem__"):
            pk_value = Car['Maker'].pk
            maker_inst = Maker.objects.get(pk=pk_value)
            return maker_inst.Make_Name
        else:
            return Car.Maker.Make_Name
        return None

    def get_Rates(self, Car):
        rates = Rate.objects.filter(Car=Car).aggregate(Avg('Value'))['Value__avg']
        if rates == None:
            rates = 'N/A'
        return rates

    class Meta:
        model = Car
        fields = ('Make_ID',
                  'Make_Name',
                  'Model_ID',
                  'Model_Name',
                  'Maker',
                  'Rates')
