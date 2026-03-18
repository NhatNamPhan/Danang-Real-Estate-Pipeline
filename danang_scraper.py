import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import random
from playwright.sync_api import sync_playwright

BASE_URL = "https://batdongsan.com.vn/nha-dat-ban-tp-da-nang"
TOTAL_PAGES = 200

def extract_product_data(product):
    try:
        # Lấy title
        title_elem = product.find(class_="pr-title")
        if not title_elem:
            title_elem = product.find(class_="re__card-title")
        title = title_elem.get_text(strip=True) if title_elem else "-"
        
        # Lấy giá
        price_elem = product.find(class_="re__card-config-price")
        price = price_elem.get_text(strip=True) if price_elem else "-"
        
        # Lấy diện tích
        area_elem = product.find(class_="re__card-config-area")
        area = area_elem.get_text(strip=True) if area_elem else "-"
        
        posted_elem = product.find(class_="re__card-published-info-published-at")
        posted = posted_elem.get_text(strip=True) if posted_elem else "-"
        
        if title == "-":
            return None
            
        return {"Title": title, "Price": price, "Area": area, "Date posted": posted}
    except:
        return None

def main():
    records = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",  # Giảm memory usage
                "--disable-gpu",  # Tắt GPU acceleration
                "--no-sandbox"  # Tắt sandbox
            ]
        )
        
        for page_num in range(1, TOTAL_PAGES + 1):
            page = None
            try:
                url = BASE_URL if page_num == 1 else f"{BASE_URL}/p{page_num}"
                
                # Progress output mỗi 50 pages
                if page_num % 50 == 0 or page_num <= 5:
                    print(f"Scraping page {page_num}/{TOTAL_PAGES}: {url}")
                
                # Tạo page mới
                page = browser.new_page(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                page.set_default_timeout(25000)
                
                # Load trang
                page.goto(url, wait_until="domcontentloaded", timeout=25000)
                time.sleep(random.uniform(1, 2))  # Giảm delay xuống
                
                # Lấy HTML
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                products = soup.find_all(class_="js__card")
                
                if products:
                    for product in products:
                        data = extract_product_data(product)
                        if data:
                            records.append(data)
                    
                    if page_num % 50 == 0:
                        print(f"  ✓ Lấy {len(products)} sản phẩm (Tổng: {len(records)})")
                
                # Đóng page ngay để giải phóng memory
                page.close()
                
            except Exception as e:
                if page:
                    try:
                        page.close()
                    except:
                        pass
                print(f"  ✗ Lỗi page {page_num}: {str(e)[:50]}")
                time.sleep(1)
                continue
        
        # Đóng browser
        browser.close()
    
    # Lưu CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"data/raw/danang_real_estate_{timestamp}.csv"
    
    with open(output_file, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Area", "Date posted"])
        writer.writeheader()
        writer.writerows(records)

    print(f"\n✓ Hoàn thành! Lưu {len(records)} sản phẩm vào: {output_file}")

if __name__ == "__main__":
    main()