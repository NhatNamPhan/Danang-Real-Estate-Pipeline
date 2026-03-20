import requests

url = "https://batdongsan.com.vn/nha-dat-ban-tp-da-nang"
res = requests.get(url)

print(res.text[:1000])