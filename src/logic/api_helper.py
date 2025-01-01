import json
import requests
from src.logic.common_utils import logging

base_url = "https://salescaller.io"


def login_and_get_token():
    payload = {
        "mobile": "9123456789",
        "password": "12345678",
        "fcm_token": None,
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()

        if data["success"]:
            return data["data"]["token"]
        else:
            return None
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        return None




def check_permission(product_id, token=None):

    if token is None :
     bearer_token = login_and_get_token()
    else:
       bearer_token = token

    headers = {"Authorization": f"Bearer {bearer_token}"}

    try:
        response = requests.get(f"{base_url}/api/v1/get-products?company_id=666", headers=headers)
        response.raise_for_status()

        data = json.loads(response.content)

        if not isinstance(data['data'], list):
            raise ValueError("Unexpected data format: 'data' should be a list")

        return any(product['id'] == product_id for product in data['data'])

    except (requests.exceptions.RequestException, json.JSONDecodeError, ValueError) as e:
        return False


def upload_file(excel_path):
    api_url = f"{base_url}/api/v1/upload-attachments"
    bearer_token = login_and_get_token()
    product_id = 981
    # contact_id = 120492 # For live env
    contact_id = 120491  # Demo
    files = []
    file_path = excel_path

    if not file_path:
        return
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    files.append(('attachments[]', open(file_path, 'rb')))

    data = {
        'contact_id': contact_id,
        'product_id': product_id
    }
    if check_permission(product_id, bearer_token):
     response = requests.post(api_url, headers=headers, data=data, files=files)
     response_data = json.loads(response.text)
     url = response_data["data"]["url"]
     logging.info(f"URL : {url}")
    return True





# Example usage (assuming you have bearer_token and api_url set)
# product_id_to_check = 55
# is_available = check_permission(product_id_to_check)
#
# if is_available:
#     print(f"Product with ID {product_id_to_check} is available.")
# else:
#     print(f"Product with ID {product_id_to_check} not found.")
