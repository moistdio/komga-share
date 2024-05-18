import requests
from requests.auth import HTTPBasicAuth

class KomgaApi:
	def __init__(self, base_url, username, password):
		self.base_url = base_url
		self.username = username
		self.password = password

	def get_series(self):
		try:
			response = requests.get(f'{self.base_url}/api/v1/series', auth=HTTPBasicAuth(self.username, self.password))
			response.raise_for_status()  # Raise an exception if the request was not successful
			return response.json()
		except requests.exceptions.RequestException as e:
			print(f"Error retrieving series: {e}")
			return None

	def get_series_by_id(self, series_id):
		try:
			response = requests.get(f'{self.base_url}/api/v1/series/{series_id}', auth=HTTPBasicAuth(self.username, self.password))
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			print(f"Error retrieving series by ID: {e}")
			return None

	def get_books(self):
		try:
			response = requests.get(f'{self.base_url}/api/v1/books', auth=HTTPBasicAuth(self.username, self.password))
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			print(f"Error retrieving books: {e}")
			return None

	def get_book_by_id(self, book_id):
		try:
			response = requests.get(f'{self.base_url}/api/v1/books/{book_id}', auth=HTTPBasicAuth(self.username, self.password))
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			print(f"Error retrieving book by ID: {e}")
			return None
		
	def get_file(self, book_id):
		try:
			response = requests.get(f'{self.base_url}/api/v1/books/{book_id}/file', auth=HTTPBasicAuth(self.username, self.password))
			# response is a octet-stream, so we save the file
			return response.content
		except requests.exceptions.RequestException as e:
			print(f"Error retrieving file: {e}")
			return None