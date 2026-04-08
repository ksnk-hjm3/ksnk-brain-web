import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [設定エリア] ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# --- [デザイン：Readdy AI風モダンデザイン] ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078" crossorigin="anonymous"></script>
    <title>K-Brain | リハと看護を繋ぐ臨床知能</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=Noto+Sans+JP:wght@300;400;700&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #f1f5f9; color: #1e293b; }
        .watermark { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80%; max-width: 600px; opacity: 0.03; z-index: -1; pointer-events: none; }
        .glass-card { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(203, 213, 225, 0.5); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); }
        html { scroll-behavior: smooth; }
    </style>
</head>
<body class="min-h-screen flex flex-col">
    <svg class="watermark" viewBox="0 0 100 100" fill="currentColor">
        <path d="M50 10 C35 10 25 25 25 45 C25 65 40 70 45 85 L55 85 C60 70 75 65 75 45 C75 25 65 10 50 10 Z" fill="none" stroke="currentColor" stroke-width="1.5"/>
    </svg>

    <header class="fixed top-0 left-0 w-full z-50 glass-card">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <h1 class="text-3xl font-extrabold tracking-tighter text-slate-900 italic">K-Brain</h1>
            <nav class="flex items-center space-x-6 text-sm font-medium text-slate-700">
                <a href="#vision" class="hover:text-sky-600 transition">Vision</a>
                <a href="https://ksnk-brain.jp" class="px-5 py-2.5 bg-sky-600 text-white rounded-full text-xs font-bold hover:bg-sky-700 transition">検索エンジン</a>
            </nav>
        </div>
    </header>

    <main class="flex-grow pt-32 p-6 md:p-12 text-center">
        <section id="vision" class="max-w-7xl mx-auto space-y-8 py-20">
            <div class="inline-block px-4 py-1.5 bg-sky-100 text-sky-700 rounded-full text-xs font-bold uppercase">Clinical Intelligence</div>
            <h2 class="text-6xl md:text-7xl font-extrabold tracking-tighter text-slate-950 leading-tight">視点が重なるとき、<br>臨床は変わる。</h2>
            <form action="/search" method="GET" class="max-w-2xl mx-auto relative mt-8">
                <input type="text" name="q" placeholder="キーワードで検索..." class="w-full p-5 bg-white rounded-2xl glass-card text-lg focus:outline-none focus:ring-2 focus:ring-sky-500 transition">
                <button type="submit" class="absolute right-4 top-4 text-sky-600 font-bold">検索</button>
            </form>
        </section>
    </main>

    <footer class="glass-card py-8 text-center text-[10px] text-slate-400 tracking-widest uppercase">
        &copy; 2026 K-BRAIN NEXUS PROJECT | MEDICAL INTELLIGENCE
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return render_template_string(INDEX_HTML)
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT title, abstract, url, source FROM papers WHERE title ILIKE %s OR abstract ILIKE %s ORDER BY id DESC LIMIT 50", (f'%{query}%', f'%{query}%'))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        results_html = f'''
        <body style="background:#f1f5f9; color:#1e293b; font-family:sans-serif; padding:20px;">
            <div style="max-width:800px; margin:0 auto; background:white; padding:30px; border-radius:15px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <h2 style="color:#0ea5e9;">「{query}」の解析結果 ({len(rows)}件)</h2>
                <a href="/" style="color:#64748b; text-decoration:none; font-size:0.9em;">← 検索画面に戻る</a><hr style="border:0; border-top:1px solid #f1f5f9; margin:20px 0;">
                {"".join([f'<div style="margin-bottom:25px; border-bottom:1px solid #f1f5f9; padding-bottom:15px;"><strong>{r[0]}</strong><p style="font-size:0.85em; color:#475569; margin:10px 0;">{r[1] or "詳細データは外部リンクを確認してください。"}</p><a href="{r[2]}" target="_blank" style="color:#0ea5e9; font-size:0.8em; text-decoration:none; font-weight:bold;">[文献エビデンスを開く]</a></div>' for r in rows])}
            </div>
        </body>
        '''
        return results_html
    except Exception as e:
        return f"Database Connection Error: {str(e)}"

if __name__ == '__main__':
    # host='0.0.0.0' を追加しました。これでRenderが通信できるようになります。
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
