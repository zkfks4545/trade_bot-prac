import os
import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

APP_KEY = os.getenv("HANTU_APP_KEY")
APP_SECRET = os.getenv("HANTU_APP_SECRET")
CANO = os.getenv("HANTU_CANO")
ACNT_PRDT_CD = os.getenv("HANTU_ACNT_PRDT_CD")
BASE_URL = "https://openapi.koreainvestment.com:9443"  # 실전 서버

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def get_access_token():
    """한투 API 접근 토큰 발급 (자동 재시도 포함)"""
    url = f"{BASE_URL}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    data = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "secretkey": APP_SECRET
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    raise Exception(f"토큰 발급 실패: {response.text}")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
def get_current_price(token, ticker):
    """특정 미국 주식의 실시간 현재가 조회"""
    url = f"{BASE_URL}/uapi/overseas-stock/v1/trading/inquire-price"
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "HHDFS00000300"  # 해외주식 현재체결가 조회 TR ID
    }
    params = {
        "AUTH": "",
        "EXCD": "NAS",  # 나스닥 기준 (필요시 NYSE, AMS 등 대응 가능)
        "SYMB": ticker
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return float(response.json().get("output", {}).get("last", 0.0))
    return None

def order_decimal_buy(token, ticker, amount_usd):
    """소수점 시장가 매수 주문 전송"""
    # 실제 소수점 주문은 한투 API 명세서의 '해외주식 소수점 예약/즉시 주문' TR ID(TTTT1006U 등)를 확인하여 구현합니다.
    print(f"🛒 [주문 송신] {ticker} 종목을 {amount_usd}달러 만큼 소수점 매수 주문합니다.")
    # API 호출 로직 생략 (실전 연결 시 가이드에 맞게 json body 매핑 필요)
    return True