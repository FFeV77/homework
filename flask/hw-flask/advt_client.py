import requests

URL = '127.0.0.1'
PORT = '5000'
link = ''.join(['http://', URL, ':', PORT])

s = requests.Session()
respsonse = s.post(link + '/user/login', json={'name': 'five', 'pwd': 'test'})
print(respsonse.status_code)
print(respsonse.text)
respsonse = s.post(link + '/advert', json={'title': 'authorized', 'description': 'third desc'})
print(respsonse.status_code)
print(respsonse.text)
respsonse = s.get(link + '/advert/14')
print(respsonse.status_code)
print(respsonse.text)
respsonse = s.patch(link + '/advert/14', json={'description': 'new_desc'})
print(respsonse.status_code)
print(respsonse.text)
respsonse = s.get(link + '/advert/14')
print(respsonse.status_code)
print(respsonse.text)
respsonse = s.delete(link + '/advert/14')
print(respsonse.status_code)
print(respsonse.text)
respsonse = requests.get(link + '/advert/14')
print(respsonse.status_code)
print(respsonse.text)

# respsonse = requests.post(link + '/user/register', json={'name': 'five', 'email': 'test@test.ru', 'pwd': 'test'})
# print(respsonse.status_code)
# print(respsonse.text)
# respsonse = requests.post(link + '/user/register', json={'name': 'second'})
# print(respsonse.status_code)
# print(respsonse.text)
# respsonse = requests.post(link + '/user/login', json={'name': 'five', 'pwd': 'dfghjkjhgfd1'})
# print(respsonse.status_code)
# print(respsonse.text)
# respsonse = requests.post(link + '/user/login', json={'name': 'five', 'pwd': 'test'})
# print(respsonse.status_code)
# print(respsonse.text)
# respsonse = requests.post(link + '/user/logout')
# print(respsonse.status_code)
# print(respsonse.text)
# respsonse = requests.get(link + '/advert/9')
# print(respsonse.status_code)
# print(respsonse.text)