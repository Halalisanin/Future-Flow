#!/usr/bin/env python3
"""
Future Flow – stealth stats & form collector
Run:  python app.py
"""
import os, sqlite3, time, pathlib
from datetime import datetime
from flask import Flask, request, g, send_from_directory

DB_FILE    = "stats.db"
SECRET_KEY = os.getenv("DASH_KEY", "SUPER_SECRET_KEY")   # <- change me

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

# ------------------------------------------------------------------ bootstrap static files
def ensure_static():
    static = pathlib.Path("static")
    static.mkdir(exist_ok=True)

    # 1. CSS you just supplied
    css = static / "style.css"
    if not css.exists():
        css.write_text("""/*  Future Flow – your supplied style.css  */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
    overflow-x: hidden;
}
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    padding: 1rem 0;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.nav-logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: #2c5aa0;
}
.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}
.nav-link {
    text-decoration: none;
    color: #333;
    font-weight: 500;
    transition: color 0.3s ease;
}
.nav-link:hover {
    color: #2c5aa0;
}
.hero {
    background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('background.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
    padding: 2rem;
}
.hero-content {
    max-width: 600px;
}
.profile-img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    border: 4px solid white;
    margin-bottom: 1.5rem;
    object-fit: cover;
}
.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-weight: 300;
}
.hero p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}
.social-links {
    margin-top: 2rem;
}
.social-link {
    display: inline-block;
    padding: 12px 30px;
    background: #2c5aa0;
    color: white;
    text-decoration: none;
    border-radius: 25px;
    transition: all 0.3s ease;
    font-weight: 500;
}
.social-link:hover {
    background: #1e3d72;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}
.blog-section {
    padding: 5rem 0;
    background: #f8f9fa;
}
.blog-section h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
    color: #333;
}
.blog-posts {
    display: grid;
    gap: 2rem;
    max-width: 800px;
    margin: 0 auto;
}
.blog-post {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    position: relative;
}
.blog-post:hover {
    transform: translateY(-5px);
}
.blog-post h3 {
    color: #2c5aa0;
    margin-bottom: 1rem;
    font-size: 1.3rem;
    line-height: 1.4;
}
.blog-post p {
    color: #666;
    margin-bottom: 0;
    line-height: 1.6;
}
.blog-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
}
.author-img {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-right: 12px;
    object-fit: cover;
}
.author-info {
    display: flex;
    flex-direction: column;
}
.author-name {
    font-weight: 600;
    color: #333;
    font-size: 0.9rem;
}
.post-date {
    color: #999;
    font-size: 0.8rem;
}
.read-more {
    display: inline-block;
    color: #2c5aa0;
    text-decoration: none;
    font-weight: 500;
    margin-top: 1rem;
    transition: color 0.3s ease;
    padding: 8px 16px;
    border: 1px solid #2c5aa0;
    border-radius: 5px;
    font-size: 0.9rem;
}
.read-more:hover {
    color: white;
    background: #2c5aa0;
    text-decoration: none;
}
.contact-section {
    padding: 5rem 0;
    background: white;
}
.contact-section h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
    color: #333;
}
.contact-form {
    max-width: 600px;
    margin: 0 auto;
}
.form-group {
    margin-bottom: 1.5rem;
}
.form-group input,
.form-group textarea {
    width: 100%;
    padding: 12px;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
    font-family: inherit;
}
.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #2c5aa0;
}
.submit-btn {
    width: 100%;
    padding: 12px;
    background: #2c5aa0;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}
.submit-btn:hover {
    background: #1e3d72;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}
.footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 2rem 0;
}
@media (max-width: 768px) {
    .nav-menu {
        gap: 1rem;
    }
    .hero h1 {
        font-size: 2rem;
    }
    .hero p {
        font-size: 1rem;
    }
    .blog-section h2,
    .contact-section h2 {
        font-size: 2rem;
    }
    .container {
        padding: 0 1rem;
    }
    .blog-post {
        padding: 1.5rem;
    }
    .blog-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
    .author-img {
        margin-right: 0;
    }
    .author-info {
        flex-direction: row;
        gap: 1rem;
        align-items: center;
    }
}
@media (max-width: 480px) {
    .nav-container {
        flex-direction: column;
        gap: 1rem;
    }
    .nav-menu {
        gap: 1.5rem;
    }
    .hero {
        padding: 1rem;
        min-height: 80vh;
    }
    .profile-img {
        width: 120px;
        height: 120px;
    }
    .blog-section,
    .contact-section {
        padding: 3rem 0;
    }
}""")

    # 2. JS you supplied earlier
    js = static / "script.js"
    if not js.exists():
        js.write_text("""/*  Future Flow – your supplied script.js  */
document.querySelectorAll('a[href^="#"]').forEach(anchor=>{anchor.addEventListener('click',function(e){e.preventDefault();const t=document.querySelector(this.getAttribute('href'));if(t){t.scrollIntoView({behavior:'smooth',block:'start'});updateActiveNavLink(this.getAttribute('href'))}})});
window.addEventListener('scroll',()=>{const n=document.querySelector('.navbar');window.scrollY>100?(n.style.background='rgba(255,255,255,.98)',n.style.boxShadow='0 2px 20px rgba(0,0,0,.1)'):(n.style.background='rgba(255,255,255,.95)',n.style.boxShadow='0 2px 10px rgba(0,0,0,.1)');updateActiveNavOnScroll()});
function updateActiveNavLink(id){document.querySelectorAll('.nav-link').forEach(l=>l.classList.remove('active'));document.querySelector(`a[href="${id}"]`).classList.add('active')}
function updateActiveNavOnScroll(){const sections=document.querySelectorAll('section');let cur='';sections.forEach(s=>{const top=s.offsetTop-100,height=s.clientHeight;if(window.scrollY>=top&&window.scrollY<top+height)cur='#'+s.getAttribute('id')});document.querySelectorAll('.nav-link').forEach(l=>{l.classList.remove('active');if(l.getAttribute('href')===cur)l.classList.add('active')})}
document.getElementById('contactForm').addEventListener('submit',function(e){e.preventDefault();const data={name:document.getElementById('name').value.trim(),email:document.getElementById('email').value.trim(),message:document.getElementById('message').value.trim()};if(validateForm(data)){const btn=this.querySelector('.submit-btn'),orig=btn.textContent;btn.textContent='Sending...';btn.disabled=!0;fetch('/submit_contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(j=>{showNotification(j.message,j.status);if(j.status==='success')this.reset()}).catch(err=>showNotification('Network error','error')).finally(()=>{btn.textContent=orig;btn.disabled=!1})}}});
function validateForm(d){const re=/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;if(!d.name){showNotification('Name required','error');document.getElementById('name').focus();return!1}if(!d.email){showNotification('Email required','error');document.getElementById('email').focus();return!1}if(!re.test(d.email)){showNotification('Valid email required','error');document.getElementById('email').focus();return!1}if(!d.message){showNotification('Message required','error');document.getElementById('message').focus();return!1}if(d.message.length<10){showNotification('Message too short','error');document.getElementById('message').focus();return!1}return!0}
function showNotification(msg,type='info'){const existing=document.querySelector('.notification');existing&&existing.remove();const n=document.createElement('div');n.className=`notification notification-${type}`;n.innerHTML=`<span>${msg}</span><button class="notification-close">&times;</button>`;n.style.cssText=`position:fixed;top:100px;right:20px;background:${type==='error'?'#e74c3c':type==='success'?'#27ae60':'#3498db'};color:white;padding:15px 20px;border-radius:8px;box-shadow:0 5px 15px rgba(0,0,0,.2);z-index:10000;display:flex;align-items:center;gap:15px;max-width:400px;animation:slideInRight .3s ease;font-weight:500`;document.body.appendChild(n);setTimeout(()=>{n.style.animation='slideOutRight .3s ease';setTimeout(()=>n.remove(),300)},5e3);n.querySelector('.notification-close').addEventListener('click',()=>{n.style.animation='slideOutRight .3s ease';setTimeout(()=>n.remove(),300)})}
const style=document.createElement('style');style.textContent=`@keyframes slideInRight{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}@keyframes slideOutRight{from{transform:translateX(0);opacity:1}to{transform:translateX(100%);opacity:0}}`;document.head.appendChild(style);
document.addEventListener('DOMContentLoaded',()=>{updateActiveNavLink('#home');const hero=document.querySelector('.hero-content');hero.style.opacity='0';hero.style.transform='translateY(30px)';hero.style.transition='opacity .8s ease,transform .8s ease';setTimeout(()=>{hero.style.opacity='1';hero.style.transform='translateY(0)'},300)});
window.addEventListener('error',e=>console.error('Site error:',e.error));
window.addEventListener('load',()=>{const t=performance.timing.loadEventEnd-performance.timing.navigationStart;console.log(`Page loaded in ${t}ms`)});""")

    # 3. placeholder background image (1×1 black pixel)
    bg = static / "background.jpg"
    if not bg.exists():
        bg.write_bytes(
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb'
            b'\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f'
            b'\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0'
            b'\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        )

# ------------------------------------------------------------------ flask app
app = Flask(__name__, static_folder='static')

@app.before_first_request
def _init():
    init_db()
    ensure_static()

@app.teardown_appcontext
def _close(exc):
    if hasattr(g, '_database'):
        g._database.close()

# ---------------------------------------------------------- public routes
@app.route('/')
def home():
    get_db().execute("INSERT INTO visits(path,ip,ua,ts) VALUES(?,?,?,?)",
                     (request.path, request.remote_addr,
                      request.headers.get('User-Agent',''), int(time.time())))
    get_db().commit()
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Future Flow - Tech Insights</title>
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

# ---------------------------------------------------------- contact form receiver
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.get_json(force=True)
    get_db().execute("INSERT INTO contacts(name,email,message,ts) VALUES(?,?,?,?)",
                     (data.get('name'), data.get('email'), data.get('message'), int(time.time())))
    get_db().commit()
    return {"status": "success", "message": "Thank you! Your message was sent."}

# ---------------------------------------------------------- secret dashboard
@app.route('/dashboard')
def dashboard():
    if request.args.get('key') != SECRET_KEY:
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
