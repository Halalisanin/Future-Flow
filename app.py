#!/usr/bin/env python3
"""
Future Flow – IP-locked, env-driven secret dashboard
"""
import os, sqlite3, time, pathlib
from datetime import datetime
from flask import Flask, request, g, make_response, redirect

DB_FILE     = "stats.db"
SECRET_KEY  = os.getenv("DASH_KEY")          # <— MUST be set
MY_IP       = os.getenv("ADMIN_IP", "")      # your public IP (optional extra lock)

if not SECRET_KEY:
    raise RuntimeError("DASH_KEY environment variable is required")

COOKIE_NAME = "ff_admin"

# ------------------------------------------------------------------ helpers
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_FILE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS visits(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           path TEXT, ip TEXT, ua TEXT, ts INTEGER)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS contacts(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT, email TEXT, message TEXT, ts INTEGER)""")
        conn.commit()

# ------------------------------------------------------------------ static
def ensure_static():
    static = pathlib.Path("static")
    static.mkdir(exist_ok=True)
    # (same CSS/JS/background as before)
    css = static / "style.css"
    if not css.exists():
        css.write_text("""/* same full CSS */""")
    js = static / "script.js"
    if not js.exists():
        js.write_text("""/* same full JS */""")
    bg = static / "background.jpg"
    if not bg.exists():
        bg.write_bytes(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')

# ------------------------------------------------------------------ app
app = Flask(__name__, static_folder='static')

@app.before_first_request
def _init():
    init_db()
    ensure_static()

@app.teardown_appcontext
def _close(exc):
    if hasattr(g, '_database'):
        g._database.close()

# ---------------------------------------------------------- unlock
@app.route('/unlock')
def unlock():
    if request.args.get('key') != SECRET_KEY:
        return "Unauthorized", 401
    resp = make_response(redirect('/'))
    resp.set_cookie(COOKIE_NAME, '1', max_age=60*60*24*30)
    return resp

# ---------------------------------------------------------- home
@app.route('/')
def home():
    get_db().execute("INSERT INTO visits(path,ip,ua,ts) VALUES(?,?,?,?)",
                     (request.path, request.remote_addr,
                      request.headers.get('User-Agent', ''), int(time.time())))
    get_db().commit()
    admin_btn = ''
    if request.cookies.get(COOKIE_NAME) == '1':
        admin_btn = '<a href="/dashboard" class="admin-btn" title="Dashboard">🔓 Dashboard</a>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Future Flow</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">Future Flow</div>
            <ul class="nav-menu">
                <li><a href="#home" class="nav-link">Home</a></li>
                <li><a href="#blog" class="nav-link">Blog</a></li>
                <li><a href="#contact" class="nav-link">Contact</a></li>
            </ul>
        </div>
    </nav>

    <section id="home" class="hero">
        <div class="hero-content">
            {admin_btn}
            <img src="https://i.pravatar.cc/150" alt="Future Flow" class="profile-img">
            <h1>Future Flow</h1>
            <p>Exploring the intersection of technology and human potential</p>
            <div class="social-links">
                <a href="https://web.facebook.com/profile.php?id=61582462596721" target="_blank" class="social-link">Follow on Facebook</a>
            </div>
        </div>
    </section>

    <section id="blog" class="blog-section">
        <div class="container">
            <h2>Tech Blog</h2>
            <div class="blog-posts">
                <article class="blog-post">
                    <div class="blog-header">
                        <img src="https://i.pravatar.cc/30" alt="Halalisani Ngema" class="author-img">
                        <div class="author-info">
                            <span class="author-name">Halalisani Ngema</span>
                            <span class="post-date">October 2025</span>
                        </div>
                    </div>
                    <h3>Bootstrap Deep Dive: Beyond the Basics</h3>
                    <p>Bootstrap is often introduced as “the framework for fast, responsive websites,” but there’s much more under the hood…</p>
                    <a href="#" class="read-more">Read More</a>
                </article>
                <article class="blog-post">
                    <div class="blog-header">
                        <img src="https://i.pravatar.cc/30" alt="Halalisani Ngema" class="author-img">
                        <div class="author-info">
                            <span class="author-name">Halalisani Ngema</span>
                            <span class="post-date">October 2025</span>
                        </div>
                    </div>
                    <h3>Bootstrap Explained: How It Can Transform Your Website</h3>
                    <p>If you’ve ever built a website, you’ve probably heard of <strong>Bootstrap</strong>. It’s one of the most popular front-end frameworks…</p>
                    <a href="#" class="read-more">Read More</a>
                </article>
            </div>
        </div>
    </section>

    <section id="contact" class="contact-section">
        <div class="container">
            <h2>Get In Touch</h2>
            <form class="contact-form" id="contactForm">
                <div class="form-group"><input type="text" id="name" name="name" placeholder="Your Name" required></div>
                <div class="form-group"><input type="email" id="email" name="email" placeholder="Your Email" required></div>
                <div class="form-group"><textarea id="message" name="message" placeholder="Your Message" rows="5" required></textarea></div>
                <button type="submit" class="submit-btn">Send Message</button>
            </form>
        </div>
    </section>

    <footer class="footer">
        <div class="container"><p>&copy; 2024 Future Flow. All rights reserved.</p></div>
    </footer>

    <script src="/static/script.js"></script>
</body>
</html>"""

# ---------------------------------------------------------- contact
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.get_json(force=True)
    get_db().execute("INSERT INTO contacts(name,email,message,ts) VALUES(?,?,?,?)",
                     (data.get('name'), data.get('email'), data.get('message'), int(time.time())))
    get_db().commit()
    return {"status": "success", "message": "Thank you! Your message was sent."}

# ---------------------------------------------------------- dashboard (IP + cookie | key)
@app.route('/dashboard')
def dashboard():
    # optional IP lock
    if MY_IP and request.remote_addr != MY_IP:
        return "Forbidden", 403
    if request.cookies.get(COOKIE_NAME) != '1' and request.args.get('key') != SECRET_KEY:
        return "Unauthorized", 401
    visits = get_db().execute("SELECT * FROM visits ORDER BY ts DESC LIMIT 200").fetchall()
    msgs   = get_db().execute("SELECT * FROM contacts ORDER BY ts DESC LIMIT 200").fetchall()
    def fmt(ts): return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    html = f"""
<!DOCTYPE html><html><head><meta charset="utf-8"><title>Future Flow – Dashboard</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;margin:2rem;background:#f4f4f4;color:#333}}
h2{{color:#2c5aa0}}
table{{width:100%;border-collapse:collapse;background:#fff;margin-bottom:2rem}}
th,td{{padding:8px 12px;border:1px #ddd solid;text-align:left}}
th{{background:#eee}}
</style></head><body>
<h2>Page Views (last 200)</h2>
<table><tr><th>Time</th><th>Path</th><th>IP</th><th>User-Agent</th></tr>"""
    for v in visits:
        html += f"<tr><td>{fmt(v['ts'])}</td><td>{v['path']}</td><td>{v['ip']}</td><td>{v['ua'][:60]}</td></tr>"
    html += "</table>"

    html += "<h2>Contact Messages (last 200)</h2><table><tr><th>Time</th><th>Name</th><th>Email</th><th>Message</th></tr>"
    for m in msgs:
        html += f"<tr><td>{fmt(m['ts'])}</td><td>{m['name']}</td><td>{m['email']}</td><td>{m['message'][:80]}</td></tr>"
    html += "</table></body></html>"
    return html

# ------------------------------------------------------------------ start
if __name__ == '__main__':
    app.run(debug=True)
