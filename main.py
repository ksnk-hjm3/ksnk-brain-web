import os, sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- 【超重要】ファイル名はこれ一点！ ---
DB_PATH = "クスノキ_審査用.sqlite" 

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain | エビデンス解析</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f9f9f9; }
        .header { text-align: center; padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .search-box { text-align: center; margin: 20px 0; }
        .search-input { width: 70%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; }
        .article-card { background: #fff; padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #007bff; }
    </style>
</head>
<body>
    <div class="header"><h1>🧠 KUSUNOKI BRAIN</h1><p>11万件の医学エビデンス・深層解析</p></div>
    <div class="search-box">
        <form action="/" method="GET">
            <input type="text" name="q" class="search-input" placeholder="検索ワードを入力" value="{{ query }}">
            <button type="submit" style="padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px;">解析開始</button>
        </form>
    </div>
    <div class="content">
        {% if error %}<p style="color:red;">エラー: {{ error }}</p>{% endif %}
        {% if data %}
            {% for row in data %}<div class="article-card"><strong>{{ row[0] }}</strong><br>{{ row[1] }}</div>{% endfor %}
        {% elif query %}
            <p style="text-align:center;">該当なし（「あ」などで試してください）</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    query = request.args.get('q', '')
    data = []
    error = None
    if query:
        try:
            if not os.path.exists(DB_PATH):
                return render_template_string(HTML_LAYOUT, query=query, error=f"ファイル {DB_PATH} が見つかりません")
            
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_name = cur.fetchone()[0]
            
            # 全カラムを取得して強引に検索
            cur.execute(f"PRAGMA table_info({table_name})")
            cols = [r[1] for r in cur.fetchall()]
            search_sql = f"SELECT {cols[0]}, {cols[1]} FROM {table_name} WHERE {cols[0]} LIKE ? OR {cols[1]} LIKE ? LIMIT 10"
            cur.execute(search_sql, (f"%{query}%", f"%{query}%"))
            data = cur.fetchall()
            conn.close()
        except Exception as e:
            error = str(e)
    
    return render_template_string(HTML_LAYOUT, data=data, query=query, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
