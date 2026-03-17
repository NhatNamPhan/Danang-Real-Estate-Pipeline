from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="msedge")
        
        page = browser.new_page()
        page.goto("https://batdongsan.com.vn/nha-dat-ban-tp-da-nang", wait_until="domcontentloaded")
        
        title = page.title()
        
        print(f"Title page: {title}")
        
        browser.close()
        

if __name__ == "__main__":
    main()