import requests

URL = '127.0.0.1'
PORT = '5000'
link = ''.join(['http://', URL, ':', PORT])

respsonse = requests.post(link + '/advert/', json={'title': 'third', 'description': 'third desc'})
print(respsonse.status_code)
print(respsonse.text)
respsonse = requests.get(link + '/advert/7/')
print(respsonse.status_code)
print(respsonse.text)
respsonse = requests.patch(link + '/advert/7/', json={'description': 'new_desc'})
print(respsonse.status_code)
print(respsonse.text)
respsonse = requests.get(link + '/advert/7/')
print(respsonse.status_code)
print(respsonse.text)
respsonse = requests.delete(link + '/advert/7/')
print(respsonse.status_code)
print(respsonse.text)
respsonse = requests.get(link + '/advert/7/')
print(respsonse.status_code)
print(respsonse.text)