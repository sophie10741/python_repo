import requests

token = '7586534808:AAGIqjT4wQQ16Jl24FWgNfxaNLiRFeRsX00'
url = f'https://api.telegram.org/bot{token}/getUpdates'
res = requests.get(url)
print(res.json())