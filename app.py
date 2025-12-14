from flask import Flask, render_template, jsonify, request
import requests
import threading
import time
import smtplib
import ssl
import os

app = Flask(__name__)

alerts = {}

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

    alerts[crypto_id] = (target_price, email)
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
    while True:
        for crypto_id, (target_price, email) in list(alerts.items()):
            url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd'
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                if crypto_id in data and 'usd' in data[crypto_id]:
                    current_price = data[crypto_id]['usd']
                    if current_price >= target_price:
                        print(f"ALERT: {crypto_id} has reached the target price of ${target_price}. Current price: ${current_price}")
                        send_email(email, f"Crypto Price Alert: {crypto_id}", f"The price of {crypto_id} has reached your target of ${target_price}. The current price is ${current_price}.")
                        del alerts[crypto_id]
            except requests.exceptions.RequestException as e:
                print(f"Error fetching price for {crypto_id}: {e}")
        time.sleep(60)

if __name__ == '__main__':
    alert_thread = threading.Thread(target=check_alerts)
    alert_thread.daemon = True
    alert_thread.start()
    app.run(debug=True)
