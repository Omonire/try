from flask import Flask, render_template, jsonify, request
import requests
import smtplib
import ssl
import os
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from database import init_db, DB_PATH

app = Flask(__name__)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/crypto')
def crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data)

@app.route('/api/set_alert', methods=['POST'])
def set_alert():
    data = request.get_json()
    crypto_id = data.get('crypto_id')
    target_price = data.get('target_price')
    email = data.get('email')

    if not crypto_id or not target_price or not email:
        return jsonify({'message': 'Invalid data'}), 400

    try:
        target_price = float(target_price)
    except ValueError:
        return jsonify({'message': 'Invalid price format'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO alerts (crypto_id, target_price, email) VALUES (?, ?, ?)",
              (crypto_id, target_price, email))
    conn.commit()
    conn.close()

    return jsonify({'message': f'Alert set for {crypto_id} at ${target_price} to be sent to {email}'})

def send_email(receiver_email, subject, message):
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", 587))
    sender_email = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")

    if not sender_email or not password:
        print("Email credentials not set. Cannot send email.")
        return

    context = ssl.create_default_context()
    email_message = f"Subject: {subject}\n\n{message}"

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, email_message)
            print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_alerts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM alerts")
    alerts = c.fetchall()

    if not alerts:
        conn.close()
        return

    crypto_ids = ",".join(list(set([alert[1] for alert in alerts])))
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_ids}&vs_currencies=usd'

    try:
        response = requests.get(url)
        response.raise_for_status()
        prices = response.json()

        for alert in alerts:
            alert_id, crypto_id, target_price, email = alert
            if crypto_id in prices and 'usd' in prices[crypto_id]:
                current_price = prices[crypto_id]['usd']
                if current_price >= target_price:
                    print(f"ALERT: {crypto_id} has reached the target price of ${target_price}. Current price: ${current_price}")
                    send_email(email, f"Crypto Price Alert: {crypto_id}", f"The price of {crypto_id} has reached your target of ${target_price}. The current price is ${current_price}.")
                    c.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
                    conn.commit()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching prices: {e}")
    finally:
        conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_alerts, trigger="interval", seconds=60)
scheduler.start()
