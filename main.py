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
    <title>K-Brain | Evidence Command Center</title>
    {ADSENSE_HEAD_CODE}
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
        
        :root {{
            --bg: #030712;
            --panel: rgba(17, 24, 39, 0.7);
            --accent: #38bdf8;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --border: rgba(255, 255, 255, 0.1);
        }}

        body {{ 
            font-family: 'Inter', sans-serif; 
            margin: 0; background-color: var(--bg); color: var(--text-main);
            background-image: 
                radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0);
            background-size: 40px 40px;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* 上部バー：司令塔の雰囲気 */
        .top-nav {{
            border-bottom: 1px solid var(--border);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(10px);
            position: sticky; top: 0; z-index: 100;
        }}

        .system-status {{
            display: flex; align-items: center; gap: 10px;
            font-family: 'JetBrains Mono', monospace; font-size: 0.7em; color: var(--accent);
        }}

        .status-dot {{
            width: 8px; height: 8px; background: var(--accent);
            border-radius: 50%; box-shadow: 0 0 10px var(--accent);
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }}
        }}

        .container {{ max-width: 1000px; margin: 0 auto; padding: 60px 20px; }}

        .hero {{ text-align: center; margin-bottom: 80px; }}

        h1 {{ 
            font-size: 4.5em; font-weight: 800; letter-spacing: -0.06em; margin: 0;
            background: linear-gradient(to bottom, #fff, #94a3b8);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}

        .tagline {{ 
            font-size: 1.1em; color: var(--accent); font-weight: 400; 
            letter-spacing: 0.4em; margin-top: 5px; text-transform: uppercase;
        }}

        /* 検索セクション：コンソール風 */
        .search-console {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 32px;
            padding: 12px;
            display: flex;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(20px);
            margin: 40px 0;
        }}

        .search-input {{
            flex: 1; border: none; background: transparent; padding: 20px 30px;
            font-size: 1.2em; color: white; outline: none;
        }}

        .analyze-btn {{
            background: var(--accent); color: #000; border: none; border-radius: 24px;
            padding: 0 45px; font-weight: 800; cursor: pointer; transition: 0.3s;
            font-family: 'Inter', sans-serif; letter-spacing: 0.05em;
        }}
        .analyze-btn:hover {{ transform: scale(1.02); box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); }}

        .metrics {{
            display: flex; justify-content: center; gap: 60px; margin-top: 30px;
            font-family: 'JetBrains Mono', monospace;
        }}
        .metric-item {{ text-align: left; }}
        .metric-label {{ display: block; font-size: 0.65em; color: var(--text-sub); text-transform: uppercase; }}
        .metric-value {{ font-size: 1.2em; font-weight: 600; color: #fff; }}

        /* 結果カード */
        .article-card {{
            background: var(--panel);
            border: 1px solid var(--border);
            padding: 40px; border-radius: 24px; margin-bottom: 30px;
            transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .article-card:hover {{
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--accent);
            transform: translateY(-4px);
        }}

        .article-title {{ font-size: 1.5em; font-weight: 700; color: #fff; margin-bottom: 15px; display: block; }}
        .article-text {{ font-size: 1.05em; color: var(--text-sub); line-height: 1.9; }}

        footer {{ text-align: center; padding: 100px 0; opacity: 0.5; font-size: 0.8em; }}
        footer a {{ color: #fff; text-decoration: none; margin: 0 15px; }}

        @media (max-width: 600px) {{
            h1 {{ font-size: 3em; }}
            .search-console {{ flex-direction: column; border-radius: 24px; }}
            .analyze-btn {{ padding: 18px; margin-top: 10px; }}
            .metrics {{ gap: 20px; flex-direction: column; align-items: center; }}
        }}
    </style>
</head>
<body>
    <div class="top-nav">
        <div style="font-weight:800; font-size:1.2em; letter-spacing:-0.05em;">K-Brain</div>
        <div class="system-status">
            <div class="status-dot"></div>
            <span>ANALYZER ONLINE / DATA_SYNC: OK</span>
        </div>
    </div>

    <div class="container">
        <div class="hero">
            <p class="tagline">思考停止を解除する</p>
            <h1>K-Brain</h1>
            
            <div class="metrics">
                <div class="metric-item">
                    <span class="metric-label">Total Evidence</span>
                    <span class="metric-value">{{{{ total_count }}}}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Engine Version</span>
                    <span class="metric-value">v19.0_PRO</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Update Frequency</span>
                    <span class="metric-value">24H_AUTO</span>
                </div>
            </div>

            <form action="/" method="GET" class="search-console">
                <input type="text" name="q" class="search-input" placeholder="解析する疾患名、手技、論文キーワードを入力..." value="{{{{ query }}}}">
                <button type="submit" class="analyze-btn">ANALYZE</button>
            </form>
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
                <div style="text-align:center; padding:100px; font-family:'JetBrains Mono'; color:var(--text-sub);">
                    > NO_DATA_FOUND_IN_NEXUS
                </div>
            {{% endif %}}
        </div>
    </div>

    <footer>
        <a href="/about">ABOUT SYSTEM</a> | <a href="/privacy">PRIVACY</a> | <a href="{INSTA_URL}" target="_blank">INSTAGRAM</a>
        <p style="margin-top:20px;">&copy; 2026 {ADMIN_NAME}. High-Fidelity Evidence Analysis Engine.</p>
    </footer>
</body>
</html>
