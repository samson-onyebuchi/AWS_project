from flask import Flask, jsonify
from faker import Faker
import requests

app = Flask(__name__)
faker = Faker()

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
    base_url = 'https://fakerapi.it/api/v1/'
    endpoint = f'products?_quantity=10&category_ids={category_id}'
    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        products = response.json()
        return jsonify(products['data'])
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500