import requests
from bs4 import BeautifulSoup
import time

# Tạo session để lưu cookies
session = requests.Session()

# Headers đầy đủ
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}

session.headers.update(headers)

# Đầu tiên, request trang gốc để lấy cookies
print("1. Lấy cookies từ trang gốc...")
home_resp = session.get("https://batdongsan.com.vn/", timeout=15)
print(f"   Status: {home_resp.status_code}")
time.sleep(1)

# Sau đó request trang search
print("2. Request trang search...")
url = "https://batdongsan.com.vn/nha-dat-ban-tp-da-nang"
response = session.get(url, timeout=15)
response.encoding = 'utf-8'

print(f"   Status: {response.status_code}")
print(f"   Content length: {len(response.content)}")
print(f"   Cookies: {session.cookies}")

soup = BeautifulSoup(response.content, "html.parser")

# Test các selector khác nhau
print("\n=== Test các selector ===")

selectors = [
    ("js__card", "class"),
    ("Item", "class"),
    ("re__item", "class"),
    ("product-item", "class"),
    ("__card", "class"),
]

for selector, selector_type in selectors:
    if selector_type == "class":
        found = soup.find_all(class_=selector)
    
    print(f"{selector}: {len(found)} elements")

# In ra top content
print("\n=== Nội dung HTML (500 chars đầu) ===")
print(response.text[:500])
