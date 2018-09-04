from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def diaflow(request):
	print request.POST
	return HttpResponse('hi')