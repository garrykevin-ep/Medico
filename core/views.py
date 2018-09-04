from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.

JSON_PAYLOAD={
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "this is a simple response from web hook"
            }
          }
        ]
      }
    }
  }
}


def diaflow(request):
	# if request.method == 'POST':	
	res = "this is a simple response from web hook"
	return JsonResponse({'fulfillmentText': res})
	return JsonResponse(JSON_PAYLOAD)
	return HttpResponse('hi')