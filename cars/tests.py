from django.test import TestCase,Client
from django.urls import reverse
from mixer.backend.django import mixer
import json
from cars import views
from cars.models import Maker,Car,Rate

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_cars_list_GET(self):
        response = self.client.get(reverse(views.car_list))
        self.assertEquals(response.status_code,200)

    def test_popular_list_GET(self):
        response = self.client.get(reverse(views.popular))
        self.assertEquals(response.status_code,200)

    def test_cars_list_POST_add_new_car(self):
        response = self.client.post(reverse(views.car_list), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING'
        },content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Car.objects.count(), 1)

    def test_cars_list_POST_add_new_car_duplicate(self):
        response = self.client.post(reverse(views.car_list), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING'
        },content_type="application/json")
        self.assertEquals(Car.objects.count(), 1)
        response2 = self.client.post(reverse(views.car_list), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING'
        },content_type="application/json")
        self.assertEquals(response2.status_code, 400)
        self.assertEquals(Car.objects.count(), 1)

    def test_cars_list_POST_add_new_car_not_available(self):
        response = self.client.post(reverse(views.car_list), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3222249,
            'Model_Name': 'GOLDWING'
        },content_type="application/json")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(Car.objects.count(), 0)
        self.assertEquals(response.json(),{"Error": "Car data invalid."})

    def test_cars_list_POST_add_new_car_maker_doesnt_exists(self):
        response = self.client.post(reverse(views.car_list), data={
            'Make_ID': 4274,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING'
        },content_type="application/json")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(Car.objects.count(), 0)
        self.assertEquals(response.json(),{"Error": "Car data invalid."})

    def test_rates_POST_car_not_found(self):
        response = self.client.post(reverse(views.car_list), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING'
        },content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Car.objects.count(), 1)
        response = self.client.post(reverse(views.rates), data={
            'Make_ID': 4724,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING',
            'Rate': 5
        },content_type="application/json")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.json(),{'Error': "{'Car': ['This field cannot be null.']}"})
        self.assertEquals(Rate.objects.count(), 0)

    def test_rates_POST_outside_limit_lower(self):
        response = self.client.post(reverse(views.car_list), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING'
        },content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Car.objects.count(), 1)
        response2 = self.client.post(reverse(views.rates), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING',
            'Rate': 0
        },content_type="application/json")
        self.assertEquals(response2.status_code, 400)
        self.assertEquals(response2.json(),{'Error': "{'Value': ['Ensure this value is greater than or equal to 1.']}"})
        self.assertEquals(Rate.objects.count(), 0)

    def test_rates_POST_outside_limit_upper(self):
        response = self.client.post(reverse(views.car_list), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING'
        },content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Car.objects.count(), 1)
        response2 = self.client.post(reverse(views.rates), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING',
            'Rate': 6
        },content_type="application/json")
        self.assertEquals(response2.status_code, 400)
        self.assertEquals(response2.json(),{'Error': "{'Value': ['Ensure this value is less than or equal to 5.']}"})
        self.assertEquals(Rate.objects.count(), 0)

    def test_rates_POST_in_limit_upper(self):
        response = self.client.post(reverse(views.car_list), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING'
        },content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Car.objects.count(), 1)
        response2 = self.client.post(reverse(views.rates), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING',
            'Rate': 5
        },content_type="application/json")
        self.assertEquals(response2.status_code, 201)
        self.assertEquals(response2.json(),{'Status': 'Successful'})
        self.assertEquals(Rate.objects.count(), 1)

    def test_rates_POST_in_limit_lower(self):
        response = self.client.post(reverse(views.car_list), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING'
        },content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Car.objects.count(), 1)
        response2 = self.client.post(reverse(views.rates), data={
            'Make_ID': 474,
            'Make_Name': 'HONDA',
            'Model_ID': 3249,
            'Model_Name': 'GOLDWING',
            'Rate': 1
        },content_type="application/json")
        self.assertEquals(response2.status_code, 201)
        self.assertEquals(response2.json(),{'Status': 'Successful'})
        self.assertEquals(Rate.objects.count(), 1)
