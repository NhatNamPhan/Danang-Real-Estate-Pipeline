from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="msedge")
        
        page = browser.new_page()
        page.goto("https://batdongsan.com.vn/nha-dat-ban-tp-da-nang")
        
        page.wait_for_selector(".js__card")
        products = page.query_selector_all(".js__card")
        
        print("=" * 50)
        print("Extracted products")
        print("=" * 50)
        
        for product in products:
            name_element = (
                product.query_selector(".pr-title") or          # card thường
                product.query_selector(".re__card-title") or    # card VIP
                product.query_selector("h3") or                 # fallback
                product.query_selector("h2")
            )
            name = name_element.inner_text() if name_element else "-"
        
            price_element = product.query_selector(".re__card-config-price")
            price = price_element.inner_text() if price_element else "-"
            
            area_element = product.query_selector(".re__card-config-area")
            area = area_element.inner_text() if area_element else "-"
            
            print(f"Product: {name}")
            print(f"Price: {price}")
            print(f"Area: {area}")
            print("=" * 30)
            
        print("\n" + "=" * 50)
        print("Using playwright locators")
        print("-" * 30)
        
        product_links = page.query_selector_all(".js__product-link-for-product-id")
        print(f"Found {len(product_links)} product links")
        
        for link in product_links:
            print(link.get_attribute("href"))
                    
        browser.close()
        

if __name__ == "__main__":
    main()