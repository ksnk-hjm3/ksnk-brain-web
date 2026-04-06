import os, sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# データベース設定
DB_PATH = "クスノキ_審査用.sqlite" 
ADMIN_NAME = "クスノキ"
INSTA_URL = "https://www.instagram.com/ksnk.hjm3/"

# --- デザインとレイアウト ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain | エビデンス解析</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f9f9f9; color: #333; }
        .header { text-align: center; padding: 30px 20px; background: #fff; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .search-box { text-align: center; margin: 30px 0; }
        .search-input { width: 70%; padding: 15px; border: 1px solid #ddd; border-radius: 30px; font-size: 16px; outline: none; }
        .article-card { background: #fff; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #2c3e50; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        footer { text-align: center; margin-top: 50px; padding: 20px; font-size: 12px; color: #777; border-top: 1px solid #eee; }
        footer a { color: #777; text-decoration: none; margin: 0 10px; }
        .btn { padding: 15px 25px; background: #2c3e50; color: white; border: none; border-radius: 30px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 KUSUNOKI BRAIN</h1>
        <p>11万件の医学エビデンス・深層解析システム</p>
    </div>

    {% block content %}
    <div class="search-box">
        <form action="/" method="GET">
            <input type="text" name="q" class="search-input" placeholder="疾患名や手技を入力（例：膝、リハ）" value="{{ query }}">
            <button type="submit" class="btn">解析</button>
        </form>
    </div>
    <div class="content">
        {% if data %}
            {% for row in data %}<div class="article-card"><strong>{{ row[0] }}</strong><br><small>{{ row[1] }}</small></div>{% endfor %}
        {% elif query %}
            <p style="text-align:center;">該当データが見つかりませんでした。</p>
        {% endif %}
    </div>
    {% endblock %}

    <footer>
        <p>&copy; 2026 {{ admin_name }}. All Rights Reserved.</p>
        <a href="/about">当サイトについて</a> | 
        <a href="/privacy">プライバシーポリシー</a> | 
        <a href="{{ insta_url }}" target="_blank">お問い合わせ(Instagram)</a>
    </footer>
</body>
</html>
"""

# --- 各種ページの設定 ---
@app.route("/")
def index():
    query = request.args.get('q', '')
    data = []
    if query:
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_name = cur.fetchone()[0]
            cur.execute(f"PRAGMA table_info({table_name})")
            cols = [r[1] for r in cur.fetchall()]
            search_sql = f"SELECT {cols[0]}, {cols[1]} FROM {table_name} WHERE {cols[0]} LIKE ? OR {cols[1]} LIKE ? LIMIT 10"
            cur.execute(search_sql, (f"%{query}%", f"%{query}%"))
            data = cur.fetchall()
            conn.close()
        except: pass
    return render_template_string(HTML_LAYOUT, data=data, query=query, admin_name=ADMIN_NAME, insta_url=INSTA_URL)

@app.route("/about")
def about():
    content = """<h2>当サイトについて</h2><p>理学療法士の知見とAI技術を融合させ、膨大な医学文献から必要な情報を瞬時に抽出するエビデンス解析ツールです。</p>"""
    return render_template_string(HTML_LAYOUT.replace('{% block content %}', content).replace('{% endblock %}', ''), admin_name=ADMIN_NAME, insta_url=INSTA_URL)

@app.route("/privacy")
def privacy():
    content = f"""<h2>プライバシーポリシー</h2>
    <p>当サイトでは、Googleによるアクセス解析ツール「Googleアナリティクス」を使用しています。また、第三者配信の広告サービス（Googleアドセンス）を利用し、ユーザーの興味に応じた広告を表示するためにCookieを使用することがあります。</p>
    <p>運営者: {ADMIN_NAME}</p>"""
    return render_template_string(HTML_LAYOUT.replace('{% block content %}', content).replace('{% endblock %}', ''), admin_name=ADMIN_NAME, insta_url=INSTA_URL)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
