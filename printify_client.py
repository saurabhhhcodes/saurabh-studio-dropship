import os
import json
import base64
import subprocess
import urllib.request

PRINTIFY_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImE0OTk1MzgzMzc3ZWIxNDFjMDU5OTcxYjEyNDFhNDhiYjgyODk2NmI4NDI5OWRkNTQzZGYxNjIxYThmNzk5NWYzYjJiMjBjNjA4MWQ4ZTQwIiwiaWF0IjoxNzk0MjExMTM1LjgxNzk2NywibmJmIjoxNzk0MjExMTM1LjgxNzk2OSwiZXhwIjoxODI1NzQ3MTM1LjgxMjc3OSwic3ViIjoiMjg5OTY1OTQiLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIiwidXNlci5pbmZvIl19.htOa77t-kF9bXHoVKA-guDILs4zr5VvoN4DNl0qpLyYjFwKOP7zQY9Ur5jitibarIfAOuzed5AnKUUlnvDkHbttRvHGVkFj0TL985g5BJmqs884HcoCbwm-LM_ppZLYZ-TKqy20n9sm5HI8UsEuva3x9ULVonYoKepEwx5RHOD3pmMIRJc5cf80tNtT7w4Tci8Z_vDj1xUH4xIXZa5lfsFVBaPQJ8Gy__kSkfuH7WmaTseoGIA7fQD53w8uBbUvCSwWPckMm6li7VoKhA00kNmI0GvMFi5sCZv6OfV7yiRG9fYKppk1hAUGKzq3tf-pZfwnB5TysA5guaJ_C1c-nPuDUMFvgh7Ug7dmdW49yn_MSxUqtPPFtCAHVQcenyfCxYGeF8T8ApxaxTWK0Pw6x5jy0Oe-2LX1ODqHpVTAacBr-ulOG1p-HtNx42Puln7WVvPiD_lggG5EbdW8DDliL1OU9ziM5VFsK1UuW1Fq_xRgC2nvS4-4QjWwj8XHWVshCo9pTWK94Vd_0m6NYi6_gzhylkGsM6ar-h6rb3AmWp_BMxOmDar1L2A3MrEJj0W-faN0cdGSLO6j3cI5dJR-SR2SnXPRst3jWC1T-gxYrr3RKf3rSJCxchNkelKzIBTTC0OJSNGjcOxRR3UTMAhyrPTOF2f7dnBghMXdBe-nPsbo"
SHOP_ID = 29672212
API_BASE = "https://api.printify.com/v1"

HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def api_request(endpoint, method="GET", payload=None):
    url = f"{API_BASE}{endpoint}"
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[!] HTTP Error {e.code} on {endpoint}: {err_msg}")
        return {"error": e.code, "message": err_msg}

def get_shops():
    return api_request("/shops.json")

def get_products():
    return api_request(f"/shops/{SHOP_ID}/products.json")

def get_orders():
    return api_request(f"/shops/{SHOP_ID}/orders.json")

def upload_image(file_path):
    if not os.path.exists(file_path):
        return {"error": "file_not_found"}
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    payload = {
        "file_name": file_name,
        "contents": encoded
    }
    return api_request("/uploads/images.json", method="POST", payload=payload)

if __name__ == "__main__":
    print("Testing Printify Client...")
    shops = get_shops()
    print("Live Shops:", shops)
    products = get_products()
    print("Products Count:", len(products.get("data", [])))
