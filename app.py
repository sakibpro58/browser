import os
from flask import Flask, request, jsonify, render_template_string
from flask_talisman import Talisman
import httpx
from bs4 import BeautifulSoup  # Added for parsing HTML titles

app = Flask(__name__)

# Flask-Talisman for Security Headers
Talisman(app, content_security_policy=None)

# Home Route
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
        <h1>Super Light Browser</h1>
        <form method="GET" action="/browse">
            <label for="url">Enter URL:</label>
            <input type="text" name="url" id="url" placeholder="https://example.com" required>
            <button type="submit">Browse</button>
        </form>
        <p>Note: Enter full URLs (e.g., https://abridgeitfirm.com/evs).</p>
    </body>
    </html>
    """)

# Browsing Route
@app.route("/browse")
def browse():
    url = request.args.get("url")
    if not url.startswith("http"):
        return jsonify({"error": "Invalid URL format. Ensure it starts with http:// or https://"}), 400
    try:
        with httpx.Client() as client:
            response = client.get(url, timeout=10)
            # Extract the title from the HTML if available
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else "No Title Found"
        return jsonify({
            "status": response.status_code,
            "title": title,
            "content": response.text[:500]  # Partial content
        })
    except httpx.RequestError as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    # Bind to the PORT environment variable, default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
