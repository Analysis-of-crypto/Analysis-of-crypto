import ccxt
import pandas as pd
from datetime import datetime

# 거래소 인스턴스 생성
exchange = ccxt.binance()

# 과거 데이터 가져오기를 위한 시작 및 끝 날짜 설정
since = exchange.parse8601('2023-01-01T00:00:00Z')  # 시작 날짜
end = exchange.parse8601('2024-01-01T00:00:00Z')  # 끝 날짜 (예: 1년 후)
all_candles = []

while since < end:
    candles = exchange.fetch_ohlcv('BTC/USDT', '1d', since)
    if not candles:
        break
    last = candles[-1][0]
    all_candles += candles
    since = last + 86400000  # 다음 날짜로 이동

# 데이터 프레임 생성
df = pd.DataFrame(all_candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['date'] = pd.to_datetime(df['timestamp'], unit='ms')  # 타임스탬프를 날짜로 변환
df = df.drop(columns=['timestamp'])  # 타임스탬프 컬럼 제거

# CSV 파일로 저장
df.to_csv('btc_usdt_1year.csv', index=False)
