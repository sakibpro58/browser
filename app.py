from flask import Flask, request, jsonify, render_template_string
from flask_talisman import Talisman
from requests_html import HTMLSession

app = Flask(__name__)

# Flask-Talisman for Security Headers
Talisman(app, content_security_policy=None)

# Initialize HTMLSession
session = HTMLSession()

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
        <h1>Abridge Super Light Browser</h1>
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
        response = session.get(url)
        response.html.render(timeout=20)  # JavaScript rendering
        return jsonify({
            "status": response.status_code,
            "title": response.html.find("title", first=True).text if response.html.find("title", first=True) else "No Title Found",
            "content": response.html.html[:500]  # Partial content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
