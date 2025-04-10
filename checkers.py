import requests

url = 'https://api.pwnedpasswords.com/range/' + '5BAA6'
res = requests.get(url)
print(res)


