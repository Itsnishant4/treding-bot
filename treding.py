from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://chartink.com/screener/down-fno-3")  # Replace with your target URL
        page.wait_for_selector("#DataTables_Table_0")  # Wait for the element to appear
        data = page.locator("#DataTables_Table_0").text_content()  # Extract text
        browser.close()

    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(debug=True)
