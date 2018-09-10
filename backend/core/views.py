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
		response = add_medicine(data)#not used
	elif action == 'list.medicine':
		response = list_medicine()
	elif  action == 'cart.add':
		response = add_to_cart(data)
	elif action == 'cart.list':
		response = show_cart(data)
	elif action == 'cart.delete':
		response = reduce_medicine_cart(data)
	elif action == 'cart.medicine.delete':
		response = remove_medicine_cart(data)
	elif action == 'cart.delete.all':
		response = empty_cart(data)
	elif action == 'cart.checkout':
		response = checkout(data)
	else:
		response = 'action not specified'

	return JsonResponse({'fulfillmentText': response})

def list_medicine():
	medicines = Medicine.objects.all()
	response = 'There is '
	last_index = len(medicines)-1
	for index,medicine in enumerate(medicines):
		response += str(medicine.quantity) + ' ' + medicine.name
		if index != last_index:
			response += ' and '
	return response+' in stock'

def add_to_cart(data):
	user = data['session']
	parameters =  data['queryResult']['parameters']
	
	try:
		medicine = Medicine.objects.get(name=parameters['medicine'])
	except Medicine.DoesNotExist:
		return '{} not found'.format(parameters['medicine'])
	
	quantity = parameters['quantity']
	cart,created = Order.objects.get_or_create(user=user,approved=False)
	cart_detail,created  = OrderDetail.objects.get_or_create(order=cart,medicine=medicine)
	
	if medicine.quantity < cart_detail.quantity+int(quantity):
		#TODO verbose
		return 'Sorry we dont have that much stock'
	else:
		cart_detail.quantity += parameters['quantity']
		cart_detail.save()

	return '{} {} added to your cart'.format(medicine.name,cart_detail.quantity)


def reduce_medicine_cart(data):	
	user = data['session']
	parameters =  data['queryResult']['parameters']
	
	try:
		medicine = Medicine.objects.get(name=parameters['medicine'])
	except Medicine.DoesNotExist:
		return '{} not found'.format(parameters['medicine'])
	
	quantity = parameters['quantity']
	cart,created = Order.objects.get_or_create(user=user,approved=False)
	try:
		cart_detail  = OrderDetail.objects.get(order=cart,medicine=medicine)
	except OrderDetail.DoesNotExist:
		return 'There is no {} in your cart'.format(medicine.name)
	
	if  cart_detail.quantity - quantity < 0:
		return 'The quantity to reduce is more than the quantity in the cart'
	else:
		cart_detail.quantity -= parameters['quantity']
		cart_detail.save()
	
	if cart_detail.quantity == 0:
		cart_detail.delete()

	return '{} {} has been removed'.format(quantity,medicine.name)

def remove_medicine_cart(data):
	'''
	removes one medicine from cart
	'''
	user = data['session']
	parameters =  data['queryResult']['parameters']
	
	try:
		medicine = Medicine.objects.get(name=parameters['medicine'])
	except Medicine.DoesNotExist:
		return '{} not found'.format(parameters['medicine'])
	
	
	cart,created = Order.objects.get_or_create(user=user,approved=False)
	
	try:
		cart_detail  = OrderDetail.objects.get(order=cart,medicine=medicine)
	except OrderDetail.DoesNotExist:
		return 'There is no {} in your cart'.format(medicine.name)
	cart_detail.delete()
	
	return '{} is removed from your cart'.format(medicine.name)

def show_cart(data):
	response = 'you have '
	user = data['session']
	cart_items=OrderDetail.objects.filter(order__user=user,order__approved=False)
	last_index = len(cart_items)-1
	if last_index == -1:
		return 'There are no items in cart'
	for index,cart_item in enumerate(cart_items):
		response += str(cart_item.quantity) + ' ' + cart_item.medicine.name
		if index != last_index:
			response += ' and '
	return response+' in cart'

	
def empty_cart(data):
	user = data['session']
	cart_details = OrderDetail.objects.filter(order__user=user,order__approved=False)
	cart_details.delete()
	return 'Your cart is cleared'
	

def checkout(data):
	user = data['session']

	cart,created = Order.objects.get_or_create(user=user,approved=False)

	cart_medicines = OrderDetail.objects.filter(order=cart)
	
	if len(cart_medicines) == 0:
		return 'There are no items in your cart'

	cart_overloaded_response = 'your cart is over loaded'
	for cart_medicine in cart_medicines:
		if cart_medicine.medicine.quantity < cart_medicine.quantity:
			cart_overloaded_response += 'we only have {} but you ordered {} of {}'.format(cart_medicine.medicine.quantity,cart_medicine.quantity,cart_medicine.medicine.name)
			return cart_overloaded_response +' please reduce the quantity or delete the item from cart'
	
	#reduce stock
	for cart_medicine in cart_medicines:
		stock_medicine = cart_medicine.medicine
		stock_medicine.quantity -= cart_medicine.quantity
		stock_medicine.save()
	
	cart.approved = True
	cart.save()
	return 'Thank you, Your order {} has been placed'.format(cart.id)



def show_my_orders(data):
	pass

def add_medicine(data):
	parameters = data['queryResult']['parameters']
	try:
		medicine = Medicine.objects.get(name=parameters['medicine'])
	except:
		return '{} not found'.format(parameters['medicine'])
	medicine.quantity += parameters['quantity']
	medicine.save()
	return 'medicine added'

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
