from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



class Maker(models.Model):
    Make_ID = models.IntegerField()
    Make_Name = models.CharField(max_length=100)

class Car(models.Model):
    Maker = models.ForeignKey(Maker, on_delete=models.CASCADE, related_name="car_maker", null=False)
    Model_ID = models.IntegerField()
    Model_Name = models.CharField(max_length=100)
    class Meta:
        unique_together = [['Model_ID', 'Model_Name']]


class Rate(models.Model):
    Value = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)])
    Car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="rate_car", null=False)
