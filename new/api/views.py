from django.shortcuts import render
from myaccount.models import Account
import requests

def GetInfoClient(access_token, url_endpoint):
	headers = {
		'Authorization' : f'Bearer {access_token}'
	}

	response = requests.get(url_endpoint, headers=headers)

	if response.status_code == 200:
		return response.json()
	else:
		return None

def GetAcessToken(code):
	client_id = "u-s4t2ud-d115455920be4e8ebaa5ac2c9dcfea89a7d2ff886b63968e88281cc31bf28bc1"
	client_secret = "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"
	redirect_uri = "http://127.0.0.1:8000/api/",
	token_url = "https://api.intra.42.fr/oauth/token"

	data = {
		'grant_type' : 'authorization_code',
		'code' : code,
		'client_id' : client_id,
		'client_secret' : client_secret,
		'redirect_uri' : redirect_uri
	}

	response = requests.post(token_url, data=data)

	if response.status_code == 200:
		access_token = response.json().get('access_token')
		return access_token
	else:
		print("Echec de la demande d'access token :", response.text)
		return None

def AuthStudent(request):
	if 'code' in request.GET:
		code = request.GET['code']

		access_token = GetAcessToken(code)
		if access_token:
			reponse = GetInfoClient(access_token, "https://api.intra.42.fr/v2/me")
			ClientInfo = Account()
			ClientInfo.username = reponse['login']
			ClientInfo.email = reponse['email']
			return render(request, 'api/api.html', {'ClientInfo': ClientInfo})
	