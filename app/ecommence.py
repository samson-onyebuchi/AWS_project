from flask import Flask, jsonify
from faker import Faker
import requests
import os


app = Flask(__name__)
faker = Faker()

faker_url = os.getenv("URL")
exchange_rate_url = os.getenv('EXCHANGE_RATES_URL')

@app.route('/category/categories')
def get_categories():
    category_tree = build_category_tree()
    return jsonify(category_tree)

def build_category_tree(parent_id=None, level=0):
    categories = []
    for _ in range(3):
        category = {
            'category_id': faker.random_number(digits=5),
            'name': faker.word(),
            'level': level,
            'children': []
        }
        if parent_id is not None:
            category['product_id'] = parent_id
        if level < 2:
            category['children'] = build_category_tree(category['category_id'], level + 1)
        categories.append(category)
    return categories



@app.route('/category/<int:category_id>/products', methods=['GET'])
def retrieve_products_by_category(category_id):
    global faker_url
    base_url = faker_url
    endpoint = f'products?_quantity=10&category_ids={category_id}'
    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()  
        products = response.json()
        return jsonify(products['data'])
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500



@app.route('/product/<int:product_id>', methods=['GET'])
def retrieve_product_details(product_id):
    global faker_url
    base_url = faker_url 
    endpoint = f'products/{product_id}'
    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()  
        product = response.json()
        return jsonify(product)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    


#@app.route('/exchange-rates/', defaults={'base_currency': 'USD'})
@app.route('/exchange-rates')
def get_exchange_rates():
    global exchange_rate_url
    url = exchange_rate_url

    response = requests.get(url)

    if response.status_code == 200:
        
        data = response.json()

        rates = data["rates"]

        exchange_rates = {currency: rate for currency, rate in rates.items()}

        return jsonify(exchange_rates)
    else:
        return jsonify({"error": "Failed to retrieve exchange rates."}), 500
