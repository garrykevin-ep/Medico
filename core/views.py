from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
# Create your views here.
import json


def diaflow(request):
	res = "this is a simple response from web hook"
	data = json.loads(request.body)
	action =  data['queryResult'].get('action','')
	response = ''
	if action == 'add.medicine':
		response = add_medicine(data)
	else:
		response = 'action not specified'

	return JsonResponse({'fulfillmentText': response})

def add_medicine(data):
	parameters = data['queryResult']['parameters']
	try:
		medicine = Medicine.object.get(name=parameters['medicine'])
	except er:
		return '{} not found {}'.format(parameters['medicine'],er)
	medicine.quantity += parameters['quantity']
	medicine.save()
	return 'medicine added'

def all_stock():
	medicines = Medicine.objects.all()
	response = 'you have '
	last_index = len(medicines)-1
	for index,medicine in enumerate(medicines):
		response += str(medicine.quantity) + ' ' + medicine.name
		if index != last_index:
			response += ' and '
	return response

def stock_list(request):
	'''
	returns a json list of all medicines
	'''
	medicines = Medicine.objects.all()
	response = []
	for medicine in medicines:
		json_obj = {
		'name' : medicine.name,
		'quantity' : medicine.quantity
		}
		response.append(json_obj)
	return JsonResponse(response,safe=False)