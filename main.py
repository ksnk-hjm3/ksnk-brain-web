import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [設定エリア] ---
# スクリーンショットから取得した先生のDB接続情報
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# --- [デザイン：統合知能・道標付き] ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain | リハと看護を繋ぐ臨床知能</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=Noto+Sans+JP:wght@300;400;700&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #020617; color: #f8fafc; background-image: radial-gradient(#1e293b 1px, transparent 1px); background-size: 40px 40px; }
        .glass-card { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(51, 65, 85, 0.5); box-shadow: 0 0 20px rgba(0, 0, 0, 0.5); }
        .neon-glow { text-shadow: 0 0 10px rgba(56, 189, 248, 0.5); }
        .search-input:focus { outline: none; border-color: #38bdf8; box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }
        .tag-btn { transition: all 0.2s ease; background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(71, 85, 105, 0.5); cursor: pointer; color: #94a3b8; }
        .tag-btn:hover { background: rgba(56, 189, 248, 0.1); border-color: #38bdf8; color: #38bdf8; transform: translateY(-1px); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center p-4">
    <div class="fixed top-6 right-6 flex items-center space-x-4 text-[10px] tracking-widest text-slate-500 uppercase">
        <div class="flex items-center"><span class="w-2 h-2 bg-sky-500 rounded-full animate-pulse mr-2"></span>Analyzer Online</div>
        <div class="border-l border-slate-800 pl-4">Total Intelligence: 168,367</div>
    </div>

    <main class="w-full max-w-3xl text-center space-y-12">
        <header class="space-y-4">
            <h1 class="text-6xl font-bold tracking-tighter neon-glow italic">K-Brain</h1>
            <div class="space-y-2">
                <p class="text-xl md:text-2xl font-light text-slate-200">視点が重なるとき、臨床は変わる。</p>
                <p class="text-sm md:text-base text-slate-400 font-light tracking-wide">
                    リハビリテーションと看護の知能を統合。<br>16万件のエビデンスから、チーム医療の「根拠」を1秒で。
                </p>
            </div>
        </header>

        <section class="space-y-6">
            <form action="/search" method="GET" class="relative">
                <input type="text" name="q" placeholder="「心不全 離床 基準」「がんリハ 浮腫」「夜間せん妄」などで検索..." class="search-input w-full p-5 bg-slate-900/80 rounded-xl glass-card text-lg font-light text-slate-100 transition-all">
                <button type="submit" class="absolute right-4 top-4 text-sky-500 hover:text-sky-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                </button>
            </form>
            <div class="flex flex-wrap justify-center gap-3">
                <button onclick="location.href='/search?q=心不全リハ'" class="tag-btn px-4 py-1.5 rounded-full text-xs">心不全リハ</button>
                <button onclick="location.href='/search?q=夜間せん妄'" class="tag-btn px-4 py-1.5 rounded-full text-xs">夜間せん妄</button>
                <button onclick="location.href='/search?q=BPSD対応'" class="tag-btn px-4 py-1.5 rounded-full text-xs">BPSD対応</button>
                <button onclick="location.href='/search?q=フレイル予防'" class="tag-btn px-4 py-1.5 rounded-full text-xs">フレイル予防</button>
                <button onclick="location.href='/search?q=嚥下訓練'" class="tag-btn px-4 py-1.5 rounded-full text-xs">嚥下訓練</button>
            </div>
        </section>

        <section class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-8 border-t border-slate-900">
            <div class="space-y-1"><div class="text-sky-500 font-bold">Search</div><p class="text-[10px] text-slate-500">臨床の悩みをキーワード検索</p></div>
            <div class="space-y-1"><div class="text-sky-500 font-bold">Analyze</div><p class="text-[10px] text-slate-500">リハと看護、双方の視点で抽出</p></div>
            <div class="space-y-1"><div class="text-sky-500 font-bold">Connect</div><p class="text-[10px] text-slate-500">共通の根拠でチーム医療を強化</p></div>
        </section>
    </main>
</body>
</html>
"""

# --- [実行ロジック] ---

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return render_template_string(INDEX_HTML)
    
    conn = get_db_connection()
    cur = conn.cursor()
    # タイトルまたは要約から検索（大文字小文字無視）
    cur.execute("SELECT title, abstract, url, source FROM papers WHERE title ILIKE %s OR abstract ILIKE %s ORDER BY id DESC LIMIT 50", (f'%{query}%', f'%{query}%'))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # 簡易的な結果表示用HTML（ここはシンプルさを維持）
    results_html = f"""
    <body style="background:#020617; color:#f8fafc; font-family:sans-serif; padding:20px;">
        <h2 style="color:#38bdf8;">「{query}」の解析結果 ({len(rows)}件)</h2>
        <a href="/" style="color:#94a3b8; text-decoration:none;">← 検索に戻る</a><br><br>
        {"".join([f'<div style="border-bottom:1px solid #1e293b; padding:15px 0;"><strong>{r[0]}</strong><p style="font-size:0.8em; color:#94a3b8;">{r[1] or "要約なし"}</p><a href="{r[2]}" target="_blank" style="color:#38bdf8; font-size:0.8em;">[文献元: {r[3]}]</a></div>' for r in rows])}
    </body>
    """
    return results_html

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
