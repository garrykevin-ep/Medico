from django.shortcuts import render
from django.http import HttpResponse
import logging
# Create your views here.


def diaflow(request):
	if request.method == 'POST':
		print ""
	return HttpResponse('hi')