from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Selenium está rodando no Render!"

# Mudou de POST para GET e pega 'query' via query string (?query=...)
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "ChatGPT")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.submit()

    results = driver.find_elements(By.CSS_SELECTOR, "h3")
    titles = [r.text for r in results if r.text.strip() != ""]

    driver.quit()

    return jsonify({"results": titles[:5]})  # Retorna os 5 primeiros títulos
