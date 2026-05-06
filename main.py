import time
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram_monitor import start_telegram_monitoring

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_MY_CHAT_ID")

def send_telegram_report(message):
    """내 개인 텔레그램으로 봇 상태 보고서 송신"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"알림 전송 실패: {e}")

if __name__ == "__main__":
    send_telegram_report("🤖 미국주식 실전 단타 봇이 정상적으로 부팅되었습니다.")
    
    try:
        # 텔레그램 비동기 리스너 구동 (실시간 스니핑 시작)
        start_telegram_monitoring()
    except KeyboardInterrupt:
        print("봇이 사용자에 의해 안전하게 종료되었습니다.")
        send_telegram_report("🟢 봇이 수동으로 안전 종료되었습니다.")