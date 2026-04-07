import os, psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- 🚀 設定エリア ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/ksnk_brain"
ADMIN_NAME = "クスノキ"
INSTA_URL = "https://www.instagram.com/ksnk.hjm3/"

ADSENSE_HEAD_CODE = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078"
     crossorigin="anonymous"></script>
"""

def format_count(n):
    return "{:,}".format(n)

def get_db_count():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM vault")
        count = cur.fetchone()[0]
        conn.close()
        return format_count(count)
    except:
        return "168,247"

HTML_LAYOUT = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain | Evidence Analyzer</title>
    {ADSENSE_HEAD_CODE}
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;600;800&family=Noto+Sans+JP:wght@300;500;700&display=swap');
        
        :root {{
            --bg: #fdfdfd;
            --main: #0f172a;
            --accent: #3b82f6;
            --glass: rgba(255, 255, 255, 0.8);
            --border: #e2e8f0;
        }}

        body {{ 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            margin: 0; background-color: var(--bg); color: var(--main);
            background-image: radial-gradient(#e2e8f0 1px, transparent 1px);
            background-size: 32px 32px; /* 緻密さを演出するグリッド */
            min-height: 100vh;
        }}

        .nav-bar {{
            padding: 20px 40px; display: flex; justify-content: space-between; align-items: center;
        }}

        .logo {{ font-size: 1.5em; font-weight: 800; letter-spacing: -0.02em; }}
        .logo span {{ font-weight: 300; color: var(--accent); }}

        .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}

        .hero {{ text-align: center; padding: 80px 0 40px; }}
        
        .badge {{
            display: inline-block; padding: 4px 12px; background: #eff6ff; color: var(--accent);
            border-radius: 20px; font-size: 0.75em; font-weight: 700; margin-bottom: 15px;
            border: 1px solid #dbeafe; letter-spacing: 0.1em;
        }}

        h1 {{ font-size: 3.5em; font-weight: 800; margin: 0; letter-spacing: -0.04em; line-height: 1; }}
        .tagline {{ font-size: 1.2em; font-weight: 300; color: #64748b; margin: 15px 0 40px; letter-spacing: 0.2em; }}

        .search-wrapper {{
            background: var(--glass); backdrop-filter: blur(10px);
            border: 1px solid var(--border); border-radius: 24px;
            padding: 8px; display: flex; box-shadow: 0 20px 40px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        .search-wrapper:focus-within {{ border-color: var(--accent); box-shadow: 0 20px 40px rgba(59,130,246,0.1); }}

        .search-input {{
            flex: 1; border: none; background: transparent; padding: 20px 30px;
            font-size: 1.2em; outline: none; color: var(--main);
        }}

        .analyze-btn {{
            background: var(--main); color: white; border: none; border-radius: 18px;
            padding: 0 40px; font-weight: 700; cursor: pointer; transition: 0.2s;
        }}
        .analyze-btn:hover {{ background: var(--accent); }}

        .stats-grid {{
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 60px;
        }}
        .stat-card {{
            background: white; padding: 20px; border-radius: 16px; border: 1px solid var(--border);
            text-align: center;
        }}
        .stat-val {{ display: block; font-size: 1.4em; font-weight: 800; color: var(--main); }}
        .stat-label {{ font-size: 0.7em; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; }}

        .article-card {{
            background: white; padding: 40px; border-radius: 24px; margin-bottom: 30px;
            border: 1px solid var(--border); transition: 0.3s;
        }}
        .article-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
        .article-title {{ font-size: 1.4em; font-weight: 700; margin-bottom: 20px; display: block; line-height: 1.4; }}
        .article-text {{ font-size: 1em; color: #475569; line-height: 1.8; }}

        footer {{ text-align: center; padding: 100px 0 60px; border-top: 1px solid var(--border); margin-top: 100px; }}
        .footer-links a {{ color: #94a3b8; text-decoration: none; margin: 0 15px; font-size: 0.8em; font-weight: 600; }}
        .footer-links a:hover {{ color: var(--accent); }}

        @media (max-width: 600px) {{
            h1 {{ font-size: 2.5em; }}
            .stats-grid {{ grid-template-columns: 1fr; }}
            .search-wrapper {{ flex-direction: column; border-radius: 30px; }}
            .analyze-btn {{ padding: 15px; width: 100%; border-radius: 20px; margin-top: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="nav-bar">
        <div class="logo">K-<span>Brain</span></div>
        <div class="footer-links" style="margin:0;"><a href="{INSTA_URL}" target="_blank">INSTAGRAM</a></div>
    </div>

    <div class="container">
        <div class="hero">
            <div class="badge">SYSTEM ONLINE</div>
            <h1>K-Brain</h1>
            <p class="tagline">思考停止を解除する</p>
            
            <form action="/" method="GET" class="search-wrapper">
                <input type="text" name="q" class="search-input" placeholder="論文・疾患・手技を解析..." value="{{{{ query }}}}">
                <button type="submit" class="analyze-btn">ANALYZE</button>
            </form>

            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-val">{{{{ total_count }}}}</span>
                    <span class="stat-label">Indexed Records</span>
                </div>
                <div class="stat-card">
                    <span class="stat-val">Global</span>
                    <span class="stat-label">Evidence Source</span>
                </div>
                <div class="stat-card">
                    <span class="stat-val">Real-time</span>
                    <span class="stat-label">Analysis Logic</span>
                </div>
            </div>
        </div>

        <div class="content">
            {{% if data %}}
                {{% for row in data %}}
                <div class="article-card">
                    <span class="article-title">{{{{ row[0] }}}}</span>
                    <div class="article-text">{{{{ row[1] }}}}</div>
                </div>
                {{% endfor %}}
            {{% elif query %}}
                <div style="text-align:center; padding:100px; color:#94a3b8;">
                    <p>一致するエビデンスが見つかりませんでした。</p>
                </div>
            {{% endif %}}
        </div>
    </div>

    <footer>
        <div class="footer-links">
            <a href="/about">ABOUT</a>
            <a href="/privacy">PRIVACY</a>
            <a href="{INSTA_URL}" target="_blank">CONTACT</a>
        </div>
        <p style="color:#cbd5e1; font-size:0.7em; margin-top:30px;">&copy; 2026 {ADMIN_NAME}. All rights reserved.</p>
    </footer>
</body>
</html>
