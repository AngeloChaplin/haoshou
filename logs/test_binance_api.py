import requests

def test_binance_api():
    url = "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDC&interval=3m&limit=1"
    try:
        response = requests.get(url, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求异常: {e}")

if __name__ == "__main__":
    test_binance_api()
