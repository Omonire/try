# Real-Time Crypto Tracker

This is a full-stack web application that tracks and displays real-time cryptocurrency prices using data from the CoinGecko API. It also includes a feature to send email alerts when a cryptocurrency reaches a user-defined price threshold. The application is built with Flask and can be easily deployed to Render.

## Features

-   **Real-Time Price Tracking:** Fetches and displays live cryptocurrency prices and market data.
-   **Price Alerts:** Users can set price alerts for any of the tracked cryptocurrencies.
-   **Email Notifications:** When a target price is reached, the application sends an email notification to the user.
-   **Production Ready:** Can be deployed to any VPS or cloud server using Gunicorn.

## Project Structure

```
├── app.py               # Main Flask application file
├── database.py          # SQLite database initialization
├── requirements.txt     # Python dependencies
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

## Production Deployment

This application is designed to be run with a production-grade WSGI server like Gunicorn. Here are the general steps to deploy it on a VPS or cloud server.

**1. Set Environment Variables:**

On your server, you need to set the following environment variables. You can do this by exporting them in your shell's startup script (e.g., `~/.bashrc`) or by using a `.env` file that you load before starting the application.

-   `SENDER_EMAIL`: Your email address for sending alerts.
-   `SENDER_PASSWORD`: Your email password or an app-specific password.
-   `SMTP_SERVER`: The SMTP server for your email provider (e.g., `smtp.gmail.com`).
-   `SMTP_PORT`: The SMTP port (e.g., `587`).

**2. Run with Gunicorn:**

Once your dependencies are installed and environment variables are set, you can start the application with Gunicorn:

```bash
gunicorn --workers 4 --preload app:app
```

-   `--workers 4`: This starts 4 worker processes to handle requests. Adjust this number based on your server's CPU cores.
-   `--preload`: This is important. It ensures the `APScheduler` background task is initialized once in the parent process before the workers are forked. This prevents multiple schedulers from running and sending duplicate alerts.

**3. Best Practices (Recommended):**

For a robust production setup, consider the following:

-   **Process Manager:** Use a process manager like `systemd` or `supervisor` to manage the Gunicorn process. This will ensure your application restarts automatically if it crashes and starts on server boot.
-   **Reverse Proxy:** Run a web server like Nginx or Apache in front of Gunicorn. Nginx can handle incoming traffic, manage SSL/TLS certificates, and serve static files more efficiently, forwarding only the dynamic requests to your Gunicorn workers.
