import yfinance as yf
import pandas as pd
import ta
import smtplib
from email.mime.text import MIMEText
from telegram import Bot

# ✅ YOUR CONFIG
TELEGRAM_TOKEN = '7651952387:AAHvfHMWid5C1nvCEjWVNeeiIywjx8eMKY4'
TELEGRAM_CHAT_ID = '5675680125'
EMAIL = 'YashShah7684@gmail.com'
APP_PASSWORD = 'jjjzzoktzhxrduuu'

stock_list = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'INFY.NS', 'KOTAKBANK.NS']

# ✅ Function to send Telegram alerts
def send_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# ✅ Function to send Email alerts
def send_email(message):
    msg = MIMEText(message)
    msg['Subject'] = '📈 AI Trading Signal Alert'
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL, APP_PASSWORD)
    server.sendmail(EMAIL, EMAIL, msg.as_string())
    server.quit()

# ✅ Signal Scanner
def scan_stocks():
    alerts = []
    for stock in stock_list:
        data = yf.download(stock, period='2d', interval='5m')
        if data.empty:
            continue
        df = data.copy()

        # Indicators
        df['vwap'] = ta.volume.VolumeWeightedAveragePrice(
            high=df['High'], low=df['Low'], close=df['Close'], volume=df['Volume']
        ).vwap

        df['rsi'] = ta.momentum.RSIIndicator(df['Close'].squeeze()).rsi()

        last = df.iloc[-1]
        body = abs(last['Close'] - last['Open'])
        range_ = last['High'] - last['Low']
        lower_shadow = min(last['Open'], last['Close']) - last['Low']
        is_hammer = lower_shadow > 2 * body and body / range_ < 0.3

        if last['Close'] > last['vwap'] and last['rsi'] < 60 and is_hammer:
            alerts.append(f"📈 {stock} | VWAP breakout + RSI({last['rsi']:.1f}) + Hammer")

    message = '\n'.join(alerts) if alerts else "❌ No trade signals this cycle."
    send_telegram(message)
    send_email(message)

# ✅ Run scanner once
if __name__ == '__main__':
    scan_stocks()
