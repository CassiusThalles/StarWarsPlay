from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse
import requests, json, random

class Index(View):
	def get(self, request):
		text = "Star Wars Game"
		context = {
			'text': text
		}
		return render(request, 'planets/index.html', context)

class Hints(View):
	def get(self, request):
		#Generate a random number between 1 and 61, as 61 is the number of planets listed in the API
		randomInt = random.randint(1, 61)

		#request the data to the API
		response = self.requestToAPI(randomInt)

		#I use this function to fill context based on response['films']
		context = self.conditionalContext(response)
		return render(request, 'planets/hints.html', context)

	#The function below will be responsible for sending and retrieving request and response to the API
	#Because if I try to verify the connection causes the app to slow down, I'll let it this way so it'll 
	#maintain it's usability
	def requestToAPI(self, planetNumber):
		url = 'https://swapi.co/api/planets/{}/'.format(planetNumber)
		response = requests.get(url)
		response = response.json()
		return response

	#Because the data from the API in the function above lists planets as url, the function below will send
	#request to the api so we can retrieve the real name of the film where the planet appears
	def requestPlanetName(self, planetUrl):
		response = requests.get(planetUrl)
		response = response.json()
		return response['title']

	#because some planets does not appear in any movie, 
	#I use here the if conditional to verify if there is any movie to display
	def conditionalContext(self, response):
		context = {}
		if response['films']:
			movies_names = []
			for movie in response['films']:
				movies_names.append(self.requestPlanetName(movie))

			context = {
				'planet_name': response['name'],
				'population': response['population'],
				'climate': response['climate'],
				'films': movies_names,

			}
		else:
			context = {
				'planet_name': response['name'],
				'population': response['population'],
				'climate': response['climate'],

			}
		return context
