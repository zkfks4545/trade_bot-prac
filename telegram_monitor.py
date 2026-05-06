import os
import re
import json
import time
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 중복 거래 방지용 메모리 장부 { Ticker: Timestamp }
recent_trades = {}
DUPLICATE_INTERVAL = config["DUPLICATE_MINUTES"] * 60

# 감시할 두 핵심 채널 ID
TARGET_CHANNELS = ['kw_USA', 'stock_news_no_1']

client = TelegramClient(
    'hantu_bot_session', 
    int(os.getenv("TELEGRAM_API_ID")), 
    os.getenv("TELEGRAM_API_HASH")
)

def extract_ticker_and_check_hojae(text):
    """텍스트에서 미국 티커(대문자 2-5자)를 추출하고 호재 단어가 있는지 검사"""
    # 정규식으로 대문자 영어 단어 추출 (미국 티커용)
    tickers = re.findall(r'\b[A-Z]{2,5}\b', text)
    if not tickers:
        return None
    
    # 설정파일에 정의된 호재 키워드 검사
    is_hojae = any(keyword in text for keyword in config["HOJAE_KEYWORDS"])
    
    if is_hojae:
        return tickers[0]  # 첫 번째로 매칭된 주력 티커 반환
    return None

@client.on(events.NewMessage(chats=TARGET_CHANNELS))
async def message_handler(event):
    message_text = event.message.message
    ticker = extract_ticker_and_check_hojae(message_text)
    
    if ticker:
        current_time = time.time()
        # 중복 매매 방지 1차 가드
        if ticker in recent_trades and (current_time - recent_trades[ticker] < DUPLICATE_INTERVAL):
            print(f"⚠️ 중복 신호 스킵: {ticker} (최근 {config['DUPLICATE_MINUTES']}분 이내 거래 이력 존재)")
            return
        
        recent_trades[ticker] = current_time
        print(f"🚀 [시그널 감지!] 종목: {ticker} / 호재 뉴스 감지되어 매수 모듈로 이관합니다.")
        # 여기서 hantu_api의 매수 함수를 호출하는 비즈니스 로직을 연결합니다.

def start_telegram_monitoring():
    print("📡 텔레그램 속보 채널 감시를 시작합니다...")
    client.start()
    client.run_until_disconnected()