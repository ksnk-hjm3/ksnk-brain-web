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
    <title>K-Brain | 思考停止を解除する</title>
    {ADSENSE_HEAD_CODE}
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        :root {{
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --primary-text: #1e293b;
            --secondary-text: #64748b;
            --accent-color: #0ea5e9;
            --border-color: #e2e8f0;
        }}

        body {{ 
            font-family: 'Inter', -apple-system, sans-serif; 
            max-width: 850px; 
            margin: 0 auto; 
            padding: 40px 20px; 
            background: var(--bg-color); 
            color: var(--primary-text); 
            line-height: 1.6;
        }}

        .header {{ 
            text-align: center; 
            padding: 60px 20px; 
            margin-bottom: 40px; 
        }}

        h1 {{ 
            font-size: 3.2em; 
            font-weight: 700; 
            letter-spacing: -0.05em; 
            margin: 0; 
            color: var(--primary-text);
        }}

        .subtitle {{ 
            font-size: 1.1em; 
            color: var(--accent-color); 
            font-weight: 400; 
            letter-spacing: 0.3em; 
            margin-top: 10px;
            text-transform: uppercase;
        }}

        .count-info {{ 
            font-size: 0.85em; 
            color: var(--secondary-text); 
            margin-top: 25px;
        }}

        .search-container {{
            background: var(--card-bg);
            padding: 10px;
            border-radius: 50px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
            display: flex;
            align-items: center;
            border: 1px solid var(--border-color);
            margin-bottom: 50px;
        }}

        .search-input {{ 
            flex-grow: 1;
            border: none;
            padding: 15px 25px;
            font-size: 1.1em;
            outline: none;
            background: transparent;
            color: var(--primary-text);
        }}

        .btn {{ 
            background: var(--primary-text);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 40px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .btn:hover {{
            background: var(--accent-color);
            transform: translateY(-1px);
        }}

        .article-card {{ 
            background: var(--card-bg); 
            padding: 35px; 
            border-radius: 16px; 
            margin-bottom: 24px; 
            border: 1px solid var(--border-color);
            transition: transform 0.2s ease;
        }}

        .article-card:hover {{
            box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        }}

        .article-title {{
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 15px;
            display: block;
            color: var(--primary-text);
        }}

        .article-text {{
            font-size: 0.95em;
            color: var(--secondary-text);
        }}

        footer {{ 
            text-align: center; 
            margin-top: 100px; 
            padding: 40px; 
            font-size: 0.8em; 
            color: var(--secondary-text); 
        }}

        footer a {{ color: var(--secondary-text); text-decoration: none; margin: 0 15px; transition: color 0.2s; }}
        footer a:hover {{ color: var(--accent-color); }}

        @media (max-width: 600px) {{
            h1 {{ font-size: 2.5em; }}
            .search-container {{ border-radius: 20px; flex-direction: column; padding: 10px; }}
            .search-input {{ width: 100%; text-align: center; }}
            .btn {{ width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>K-Brain</h1>
        <p class="subtitle">思考停止を解除する</p>
        <p class="count-info">Database: <span style="font-weight:600; color:var(--primary-text); border-bottom: 2px solid var(--accent-color);">{{{{ total_count }}}}</span> Evidence Records Indexed</p>
    </div>

    {{% block content %}}
    <div class="search-box">
        <form action="/" method="GET" class="search-container">
            <input type="text" name="q" class="search-input" placeholder="論文タイトル、疾患名、手技で解析..." value="{{{{ query }}}}">
            <button type="submit" class="btn">ANALYZE</button>
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
            <p style="text-align:center; color: var(--secondary-text);">NO EVIDENCE FOUND FOR "{{{{ query }}}}"</p>
        {{% endif %}}
    </div>
    {{% endblock %}}

    <footer>
        <p>&copy; 2026 {ADMIN_NAME}. Powered by AI Evidence Analysis.</p>
        <a href="/about">ABOUT</a> 
        <a href="/privacy">PRIVACY</a> 
        <a href="{INSTA_URL}" target="_blank">INSTAGRAM</a>
    </footer>
</body>
</html>
"""

@app.route("/")
def index():
    query = request.args.get('q', '')
    total_count = get_db_count()
    data = []
    if query:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            search_sql = "SELECT title, full_text FROM vault WHERE title ILIKE %s OR full_text ILIKE %s LIMIT 20"
            cur.execute(search_sql, (f"%{query}%", f"%{query}%"))
            data = cur.fetchall()
            conn.close()
        except: pass
    return render_template_string(HTML_LAYOUT, data=data, query=query, total_count=total_count)

@app.route("/about")
def about():
    total_count = get_db_count()
    return render_template_string(HTML_LAYOUT.replace('{% block content %}', '<div class="article-card"><h2>ABOUT PROJECT</h2><p>理学療法士の現場に「根拠」と「閃き」を。16万件超のエビデンスが、あなたの臨床の思考停止を解除します。</p></div>').replace('{% endblock %}', ''), total_count=total_count)

@app.route("/privacy")
def privacy():
    total_count = get_db_count()
    return render_template_string(HTML_LAYOUT.replace('{% block content %}', f'<div class="article-card"><h2>PRIVACY POLICY</h2><p>当サイトではGoogleアドセンスを利用し、広告を配信しています。</p><p>運営者: {ADMIN_NAME}</p></div>').replace('{% endblock %}', ''), total_count=total_count)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
