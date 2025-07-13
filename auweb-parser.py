from playwright.sync_api import sync_playwright
import pandas as pd

def parse_price(price_str):
    """Parse price string like 'NOK\xa0299.00' or '0' into float value."""
    if not price_str or price_str in ['0', 'N/A']:
        return 0.0
    try:
        # Remove currency symbols and non-breaking spaces
        cleaned = price_str.replace('NOK', '').replace('\xa0', '').replace('$', '').replace('€', '').replace('£', '').strip()
        return float(cleaned.replace(',', ''))
    except Exception:
        return 0.0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Use headless=False to debug easily
    context = browser.new_context()
    page = context.new_page()

    games_list = []

    # Start listening for network requests
    def handle_response(response):
        if "graphql?operationName=searchStoreQuery" in response.url:
            if response.status == 200:
                print("✅ Found and captured response!")
                data = response.json()
                elements = data.get('data', {}).get('Catalog', {}).get('searchStore', {}).get('elements', [])
                
                for game in elements:
                    title = game.get('title')
                    mappings = game.get('catalogNs', {}).get('mappings', [])
                    slug = mappings[0].get('pageSlug') if mappings else ''
                    link = f"https://store.epicgames.com/en-US/p/{slug}" if slug else "Нет ссылки"

                    price_info = game.get('price', {}).get('totalPrice', {}).get('fmtPrice', {})
                    original_price_str = price_info.get('originalPrice', 'N/A')
                    discount_price_str = price_info.get('discountPrice', 'N/A')

                    original_price_val = parse_price(original_price_str)
                    discount_price_val = parse_price(discount_price_str)
                    savings = original_price_val - discount_price_val

                    games_list.append({
                        "Title": title,
                        "Original Price": original_price_str,
                        "Discount Price": discount_price_str,
                        "Savings": round(savings, 2),
                        "Link": link
                    })

    page.on("response", handle_response)

    print("➡️ Navigating to Epic Games Store...")
    page.goto("https://store.epicgames.com/en-US/browse?sortBy=releaseDate&sortDir=DESC&priceTier=tierDiscouted&category=Game&count=40&start=0")
    page.wait_for_timeout(10000)  # wait for JS to load requests

    print("⏳ Waiting... Scroll or interact to help load the data...")
    input("👉 Press Enter after the site loads and data appears...\n")

    # Sort games by savings descending (highest discount first)
    games_list.sort(key=lambda g: g['Savings'], reverse=True)

    # Write to Excel
    df = pd.DataFrame(games_list)
    excel_path = 'results_sorted.xlsx'
    df.to_excel(excel_path, index=False)
    print(f"📄 Data written to Excel: {excel_path}")

    # Optionally still write to .txt if needed
    txt_path = 'results-2.txt'
    with open(txt_path, 'w', encoding='utf-8') as out_file:
        for game in games_list:
            out_file.write(f"Title: {game['Title']}\n")
            out_file.write(f"Original Price: {game['Original Price']}\n")
            out_file.write(f"Discount Price: {game['Discount Price']}\n")
            out_file.write(f"Savings: {game['Savings']}\n")
            out_file.write(f"Link: {game['Link']}\n")
            out_file.write("-" * 40 + "\n")

    print(f"📄 Backup .txt written to: {txt_path}")
    browser.close()