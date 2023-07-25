from django.db import models

class Color(models.Model):
    color_name=models.CharField(max_length=100)

    def __str__(self):
        return self.color_name

class Persons(models.Model):
    color = models.ForeignKey(Color,null=True,on_delete=models.CASCADE,blank=True,related_name='color')
    name = models.CharField(max_length =100)
    age = models.IntegerField()
