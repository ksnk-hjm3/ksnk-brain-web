import os, psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- 🚀 設定エリア ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/ksnk_brain"
ADMIN_NAME = "クスノキ"
INSTA_URL = "https://www.instagram.com/ksnk.hjm3/"

# 【重要】Googleアドセンス審査用コードをここに設置しました
ADSENSE_HEAD_CODE = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078"
     crossorigin="anonymous"></script>
"""

# 広告表示用のプレースホルダー
ADS_UNIT_TOP = """<div style="text-align:center; margin:20px 0; color:#ccc; font-size:10px;">（スポンサーリンク）</div>"""
ADS_UNIT_BOTTOM = """<div style="text-align:center; margin:20px 0; color:#ccc; font-size:10px;">（スポンサーリンク）</div>"""

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
        h1 {{ margin: 0; font-size: 2.5em; color: #2c3e50; }}
        .search-box {{ text-align: center; margin: 30px 0; }}
        .search-input {{ width: 75%; padding: 18px 25px; border: 2px solid #eee; border-radius: 40px; font-size: 18px; outline: none; transition: 0.3s; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }}
        .search-input:focus {{ border-color: #3498db; box-shadow: 0 4px 20px rgba(52,152,219,0.15); }}
        .article-card {{ background: #fff; padding: 25px; border-radius: 12px; margin-bottom: 20px; border-left: 6px solid #3498db; box-shadow: 0 3px 10px rgba(0,0,0,0.05); }}
        .article-title {{ font-size: 1.2em; color: #2c3e50; margin-bottom: 10px; display: block; }}
        .article-text {{ font-size: 0.95em; color: #7f8c8d; line-height: 1.6; }}
        footer {{ text-align: center; margin-top: 60px; padding: 30px; font-size: 13px; color: #95a5a6; border-top: 1px solid #e0e0e0; }}
        footer a {{ color: #3498db; text-decoration: none; margin: 0 10px; }}
        .btn {{ padding: 18px 35px; background: #2c3e50; color: white; border: none; border-radius: 40px; cursor: pointer; font-size: 16px; margin-left: -60px; position: relative; transition: 0.3s; }}
        .btn:hover {{ background: #34495e; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 KUSUNOKI BRAIN</h1>
        <p>168,154件の医学エビデンス・深層解析システム</p>
    </div>

    {ADS_UNIT_TOP}

    {{% block content %}}
    <div class="search-box">
        <form action="/" method="GET">
            <input type="text" name="q" class="search-input" placeholder="疾患名、手技、キーワードを入力..." value="{{{{ query }}}}">
            <button type="submit" class="btn">解析</button>
        </form>
    </div>
    <div class="content">
        {{% if data %}}
            <p style="margin-bottom: 20px; color: #7f8c8d;">最新の20件を表示中...</p>
            {{% for row in data %}}
            <div class="article-card">
                <strong class="article-title">{{{{ row[0] }}}}</strong>
                <div class="article-text">{{{{ row[1] }}}}</div>
            </div>
            {{% endfor %}}
        {{% elif query %}}
            <div style="text-align:center; padding: 50px;">
                <p>「{{{{ query }}}}」に該当するエビデンスは見つかりませんでした。</p>
            </div>
        {{% endif %}}
    </div>
    {{% endblock %}}

    {ADS_UNIT_BOTTOM}

    <footer>
        <p>&copy; 2026 {ADMIN_NAME}. All Rights Reserved.</p>
        <a href="/about">当サイトについて</a> | 
        <a href="/privacy">プライバシーポリシー</a> | 
        <a href="{INSTA_URL}" target="_blank">お問い合わせ(Instagram)</a>
    </footer>
</body>
</html>
"""

@app.route("/")
def index():
    query = request.args.get('q', '')
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
    return render_template_string(HTML_LAYOUT, data=data, query=query)

@app.route("/about")
def about():
    content = """<div class="article-card"><h2>当サイトについて</h2><p>16万件を超える膨大な医学文献から必要な情報を瞬時に抽出する、プロフェッショナルのためのエビデンス解析ツールです。</p></div>"""
    return render_template_string(HTML_LAYOUT.replace('{% block content %}', content).replace('{% endblock %}', ''))

@app.route("/privacy")
def privacy():
    content = f"""<div class="article-card"><h2>プライバシーポリシー</h2>
    <p>当サイトではGoogleアドセンスを利用し、広告を配信しています。Cookieを使用してユーザーの興味に応じた広告を表示することがあります。これにより、お客様のブラウザを識別できるようになりますが、個人を特定するものではありません。</p>
    <p>運営者: {ADMIN_NAME}</p></div>"""
    return render_template_string(HTML_LAYOUT.replace('{% block content %}', content).replace('{% endblock %}', ''))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
