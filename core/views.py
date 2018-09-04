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
	if request.method == 'POST':
		print ""
	return JsonResponse(JSON_PAYLOAD)
	return HttpResponse('hi')