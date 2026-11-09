import os
import json
import urllib.request

GELATO_API_KEY = "43af8626-a562-4bbb-b5fe-9f8bae763606-3f2fd186-beaf-44d5-90cc-c28f16396a04:b140bca9-8918-43a5-ba74-c2b6129cd95b"
STORE_ID = "48c4342e-4aaf-4c2c-a075-37b6db117bce"

HEADERS = {
    "X-API-KEY": GELATO_API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def api_request(url, method="GET", payload=None):
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"[!] Gelato API Error {e.code} on {url}: {err}")
        return {"error": e.code, "message": err}

def get_stores():
    return api_request("https://ecommerce.gelatoapis.com/v1/stores")

def get_orders():
    return api_request(f"https://order.gelatoapis.com/v4/orders")

def create_order(order_payload):
    return api_request("https://order.gelatoapis.com/v4/orders", method="POST", payload=order_payload)

if __name__ == "__main__":
    print("Testing Gelato API Client...")
    stores = get_stores()
    print("Stores:", json.dumps(stores, indent=2))
