import os, sqlite3, urllib.parse
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- 【設定】データベースのファイル名 ---
# GitHubに一緒にアップロードするDBファイル名と一致させてください
DB_PATH = "クスノキ_マスターデータベース.sqlite" 

# --- 💰 収益化・アドセンス審査用 デザインテンプレート ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain | 理学療法・最新エビデンス解析</title>
    <style>
        body { font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background: #f9f9f9; }
        .header { text-align: center; padding: 30px 0; background: #fff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 5px solid #007bff; }
        .search-box { text-align: center; margin-bottom: 30px; background: #fff; padding: 20px; border-radius: 10px; }
        .search-input { width: 65%; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; outline: none; }
        .search-input:focus { border-color: #007bff; }
        .ad-banner { background: #fff; padding: 15px; text-align: center; margin: 20px 0; border: 1px dashed #bbb; color: #999; border-radius: 8px; min-height: 100px; display: flex; align-items: center; justify-content: center; }
        .article-card { background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #007bff; }
        .article-title { font-weight: bold; font-size: 1.1em; color: #007bff; margin-bottom: 8px; }
        .article-text { font-size: 0.95em; color: #555; }
        footer { text-align: center; font-size: 0.8em; color: #aaa; margin-top: 50px; padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 KUSUNOKI BRAIN</h1>
        <p>11万件の医学エビデンス・深層解析ポータル</p>
    </div>

    <div class="search-box">
        <form action="/" method="GET">
            <input type="text" name="q" class="search-input" placeholder="疾患名、治療法、最新エビデンスを検索" value="{{ query }}">
            <button type="submit" style="padding: 12px 25px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">解析開始</button>
        </form>
    </div>

    <div class="ad-banner">
        【スポンサーリンク / 広告掲載エリア】
    </div>

    <div class="content">
        {% if data %}
            <p style="margin-bottom: 15px; color: #666;">「{{ query }}」の検索結果: {{ data|length }}件</p>
            {% for row in data %}
                <div class="article-card">
                    <div class="article-title">{{ row[0] }}</div>
                    <div class="article-text">{{ row[1][:500] }}...</div>
                </div>
                {% if loop.index == 1 or loop.index == 4 %}
                    <div class="ad-banner">【記事間広告 / 収益化ユニット】</div>
                {% endif %}
            {% endfor %}
        {% else %}
            {% if query %}
                <p style="text-align:center; color:#999;">該当するデータが見つかりませんでした。別のキーワードを試してください。</p>
            {% else %}
                <div style="text-align:center; padding: 40px; color:#777;">
                    <h3>臨床知能へのアクセス</h3>
                    <p>検索窓にキーワードを入力して、K-Brainの知能を解放してください。</p>
                </div>
            {% endif %}
        {% endif %}
    </div>

    <div class="ad-banner">【フッター広告ユニット】</div>

    <footer>
        &copy; 2026 ksnk-brain.jp | Powered by K-Brain Engine v19.2<br>
        本サイトは理学療法士の臨床意思決定を支援するためのエビデンス集積プラットフォームです。
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
            # データベース接続（読み取り専用）
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            # タイトルまたは本文にキーワードが含まれるものを10件抽出
            cur.execute("SELECT title, full_text FROM vault WHERE full_text LIKE ? OR title LIKE ? ORDER BY rowid DESC LIMIT 10", (f"%{query}%", f"%{query}%"))
            data = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error connecting to DB: {e}")
    
    return render_template_string(HTML_LAYOUT, data=data, query=query)

if __name__ == "__main__":
    # Render公開用のポート設定
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)