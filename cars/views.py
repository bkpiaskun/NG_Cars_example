from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from cars.models import Car, Maker, Rate
from cars.serializers import CarsSerializer, MakerSerializer
from rest_framework.decorators import api_view
from django.db.models import Avg, Count
import requests
from django.forms.models import model_to_dict


@api_view(['GET','POST'])
def car_list(request):
    cars = Car.objects.all()
    if request.method == 'GET':
        cars_serializer = CarsSerializer(cars, many=True)
        return JsonResponse(cars_serializer.data, safe=False)
 
    elif request.method == 'POST':
        new_car_data = JSONParser().parse(request)
        Makers_available = Maker.objects.filter(Make_ID = new_car_data['Make_ID']).filter(Make_Name = new_car_data['Make_Name'])


        url_path = 'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json'.format(new_car_data['Make_Name'])
        response = requests.get(url_path)
        parsed_data = response.json()['Results']
        cars_serializer = CarsSerializer(data=new_car_data)

        if not Makers_available.exists():
            for parsed_data_item in parsed_data:
                if parsed_data_item == new_car_data:
                    Serialized_Maker = MakerSerializer(data=parsed_data_item)
                    if Serialized_Maker.is_valid():
                        Serialized_Maker.save()
                        Makers_available = Maker.objects.filter(Make_ID = new_car_data['Make_ID']).filter(Make_Name = new_car_data['Make_Name'])
                    else:
                        return JsonResponse(data={"Error": "Maker does not exists."}, status=status.HTTP_400_BAD_REQUEST)

        if Makers_available.exists():
            new_car_data['Maker'] = Makers_available.first().pk

        if cars_serializer.is_valid():
            if new_car_data not in cars:
                for parsed_data_item in parsed_data:
                    if cars_serializer.initial_data['Make_ID'] == parsed_data_item['Make_ID'] and cars_serializer.initial_data['Make_Name'] == parsed_data_item['Make_Name'] and cars_serializer.initial_data['Model_ID'] == parsed_data_item['Model_ID'] and cars_serializer.initial_data['Model_Name'] == parsed_data_item['Model_Name']:
                            cars_serializer.save()
                            return JsonResponse(cars_serializer.data, status=status.HTTP_201_CREATED) 
        else:
            return JsonResponse(data={"Error": "Car data invalid."}, status=status.HTTP_400_BAD_REQUEST)        
    
 
 
@api_view(['POST'])
def rates(request):
    request_data = JSONParser().parse(request)
    found_maker = Maker.objects.filter(Make_ID = request_data['Make_ID']).filter(Make_Name = request_data['Make_Name']).first()
    found_car = Car.objects.filter(Maker=found_maker,Model_ID=request_data['Model_ID'],Model_Name=request_data['Model_Name']).first()
    rate = Rate(Car=found_car, Value=request_data['Rate'])
    try:
        rate.full_clean()
    except ValidationError as e:
        return JsonResponse(data={"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        rate.save()
        return JsonResponse(data={"Status": "Successful"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def popular(request):
    
    Cars_by_most_rates = Rate.objects.values('Car').annotate(score=Count('Value')).order_by('-score').values_list('Car')[:3]
    cars = Car.objects.filter(id__in=Cars_by_most_rates)
    car_ser = CarsSerializer(data=cars, many=True)
    car_ser.is_valid()
    return JsonResponse(data=car_ser.data, status=status.HTTP_200_OK, safe=False)
