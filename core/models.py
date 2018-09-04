from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Medicine(models.Model):
	name = models.CharField(max_length=50)
	quantity = models.IntegerField()

	def __str__(self):
		return '{} quantities of '.format(self.quantity,self.name)

class Order(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	medicines = models.ManyToManyField(Medicine)
	

class OrderDetails(models.Model):
	order = models.ForeignKey(Order,on_delete = models.CASCADE)
	medicine = models.ForeignKey(Medicine,on_delete = models.CASCADE) 
	quantity = models.IntegerField()