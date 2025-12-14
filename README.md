# Real-Time Crypto Tracker

This is a full-stack web application that tracks and displays real-time cryptocurrency prices using data from the CoinGecko API. It also includes a feature to send email alerts when a cryptocurrency reaches a user-defined price threshold. The application is built with Flask and can be easily deployed to Render.

## Features

-   **Real-Time Price Tracking:** Fetches and displays live cryptocurrency prices and market data.
-   **Price Alerts:** Users can set price alerts for any of the tracked cryptocurrencies.
-   **Email Notifications:** When a target price is reached, the application sends an email notification to the user.
-   **Easy Deployment:** Includes a `render.yaml` file for one-click deployment to Render.

## Project Structure

```
├── app.py               # Main Flask application file
├── database.py          # SQLite database initialization
├── requirements.txt     # Python dependencies
├── render.yaml          # Render deployment configuration
├── templates/
│   └── index.html       # Frontend HTML and JavaScript
└── static/              # (Optional) For CSS and other static assets
```

## Local Setup

To run this application on your local machine, follow these steps:

**1. Clone the Repository:**

```bash
git clone <repository-url>
cd <repository-directory>
```

**2. Create a Virtual Environment:**

It's recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

**3. Install Dependencies:**

```bash
pip install -r requirements.txt
```

**4. Run the Application:**

```bash
python app.py
```

The application will be running at `http://127.0.0.1:5000`.

## Deployment to Render

This project is configured for easy deployment to [Render](https://render.com/).

**1. Fork the Repository:**

Fork this repository to your own GitHub account.

**2. Create a New Web Service on Render:**

-   Go to your Render dashboard and click "New +".
-   Select "Web Service".
-   Connect your GitHub account and select the forked repository.

**3. Configure the Web Service:**

Render will automatically detect the `render.yaml` file and configure the service for you. The application uses a SQLite database for alert storage, which is created automatically on a persistent disk.

**4. Set Environment Variables:**

For the email notification feature to work, you must set the following environment variables in your Render dashboard under the "Environment" section:

-   `SENDER_EMAIL`: Your email address for sending alerts.
-   `SENDER_PASSWORD`: Your email password or an app-specific password.
-   `SMTP_SERVER`: The SMTP server for your email provider (e.g., `smtp.gmail.com`).
-   `SMTP_PORT`: The SMTP port (e.g., `587`).

**5. Deploy:**

Click "Create Web Service" to deploy the application. Render will build and start the application automatically. Once the deployment is complete, you can access your live crypto tracker at the URL provided by Render.
