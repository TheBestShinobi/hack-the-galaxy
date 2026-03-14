import requests
import json

def test_bank_parser():
    url = "http://localhost:8000/parse/bank"
    
    # Example CSV-style data
    csv_data = "Description,Amount\nShell Service Station,55.00\nUber Trip,22.40"
    
    payload = {"data": csv_data}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        print("Success!")
        for item in response.json():
            print(f"Merchant: {item['merchant']} | CO2: {item['co2_kg']}kg")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_bank_parser()
