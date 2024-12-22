import os
from flask import Flask, request, Response, render_template_string
from flask_talisman import Talisman
import httpx

app = Flask(__name__)

# Flask-Talisman for Security Headers
Talisman(app, content_security_policy=None)

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Super Light Browser</title>
    </head>
    <body>
        <h1>AB Super Light Browser</h1>
        <form method="GET" action="/browse">
            <label for="url">Enter URL:</label>
            <input type="text" name="url" id="url" placeholder="https://example.com" required>
            <button type="submit">Browse</button>
        </form>
        <p>Note: Enter full URLs (e.g., https://abridgeitfirm.com/evs).</p>
    </body>
    </html>
    """)

@app.route("/browse")
def browse():
    url = request.args.get("url")
    if not url.startswith("http"):
        return "Invalid URL format. Ensure it starts with http:// or https://", 400
    try:
        with httpx.Client() as client:
            response = client.get(url, timeout=10)
            response.raise_for_status()
        # Forward the fetched HTML content to the client
        return Response(response.text, content_type="text/html")
    except httpx.RequestError as e:
        return f"Request failed: {str(e)}", 500
    except Exception as e:
        return f"Unexpected error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
