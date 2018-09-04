from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
# Create your views here.


def diaflow(request):
	res = "this is a simple response from web hook"
	action = request.POST['queryResult']['action']
	return JsonResponse({'fulfillmentText': action})
	return JsonResponse(JSON_PAYLOAD)

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