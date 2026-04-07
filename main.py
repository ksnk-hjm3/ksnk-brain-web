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

# 数値を「168,154」のようにカンマ区切りにする関数
def format_count(n):
    return "{:,}".format(n)

# データベースから現在の総件数を取得する関数
def get_db_count():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM vault")
        count = cur.fetchone()[0]
        conn.close()
        return format_count(count)
    except:
        return "168,154" # エラー時はとりあえず今の数字を出す

HTML_LAYOUT = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain | エビデンス解析</title>
    {ADSENSE_HEAD_CODE}
    <style>
        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f4f7f6; color: #2c3e50; }}
        .header {{ text-align: center; padding: 40px 20px; background: #fff; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 30px; }}
        .search-input {{ width: 75%; padding: 18px; border: 2px solid #eee; border-radius: 40px; font-size: 18px; outline: none; }}
        .article-card {{ background: #fff; padding: 25px; border-radius: 12px; margin-bottom: 20px; border-left: 6px solid #3498db; box-shadow: 0 3px 10px rgba(0,0,0,0.05); }}
        .btn {{ padding: 18px 35px; background: #2c3e50; color: white; border: none; border-radius: 40px; cursor: pointer; margin-left: -60px; position: relative; }}
        footer {{ text-align: center; margin-top: 60px; padding: 30px; font-size: 12px; color: #95a5a6; border-top: 1px solid #e0e0e0; }}
        footer a {{ color: #3498db; text-decoration: none; margin: 0 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 KUSUNOKI BRAIN</h1>
        <p><span style="color:#3498db; font-weight:bold;">{{{{ total_count }}}}</span> 件の医学エビデンス・深層解析システム</p>
    </div>

    {{% block content %}}
    <div class="search-box" style="text-align:center; margin-bottom:40px;">
        <form action="/" method="GET">
            <input type="text" name="q" class="search-input" placeholder="キーワードを入力..." value="{{{{ query }}}}">
            <button type="submit" class="btn">解析</button>
        </form>
    </div>
    <div class="content">
        {{% if data %}}
            {{% for row in data %}}
            <div class="article-card">
                <strong style="display:block; margin-bottom:10px;">{{{{ row[0] }}}}</strong>
                <div style="font-size:0.9em; color:#7f8c8d; line-height:1.6;">{{{{ row[1] }}}}</div>
            </div>
            {{% endfor %}}
        {{% elif query %}}
            <p style="text-align:center;">該当するエビデンスは見つかりませんでした。</p>
        {{% endif %}}
    </div>
    {{% endblock %}}

    <footer>
        <p>&copy; 2026 {ADMIN_NAME}. All Rights Reserved.</p>
        <a href="/about">当サイトについて</a> | <a href="/privacy">プライバシーポリシー</a> | <a href="{INSTA_URL}" target="_blank">お問い合わせ</a>
    </footer>
</body>
</html>
"""

@app.route("/")
def index():
    query = request.args.get('q', '')
    total_count = get_db_count() # 総件数を取得
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
    return render_template_string(HTML_LAYOUT.replace('{% block content %}', '<div class="article-card"><h2>当サイトについて</h2><p>理学療法士の知見とAI技術を融合させた、医学エビデンス解析ツールです。</p></div>').replace('{% endblock %}', ''), total_count=total_count)

@app.route("/privacy")
def privacy():
    total_count = get_db_count()
    return render_template_string(HTML_LAYOUT.replace('{% block content %}', f'<div class="article-card"><h2>プライバシーポリシー</h2><p>当サイトではGoogleアドセンスを利用し、広告を配信しています。</p><p>運営者: {ADMIN_NAME}</p></div>').replace('{% endblock %}', ''), total_count=total_count)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
