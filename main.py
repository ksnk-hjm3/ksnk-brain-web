import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [設定エリア] ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# --- [デザイン：AdSense & Conversion Optimized] ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078" crossorigin="anonymous"></script>
    <title>K-Brain | 医療職のためのエビデンス検索エンジン</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Noto+Sans+JP:wght@300;500;700&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #fafafa; color: #1a1a1a; }
        .art-bg { position: fixed; top: 45%; left: 50%; transform: translate(-50%, -50%); width: 80%; opacity: 0.08; z-index: -1; pointer-events: none; }
        .premium-card { background: white; border-radius: 24px; border: 1px solid #f1f5f9; box-shadow: 0 4px 20px rgba(0,0,0,0.03); }
        .search-pill { background: white; border-radius: 999px; box-shadow: 0 10px 40px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }
        .btn-medical { background: #A3C9D6; color: white; border-radius: 999px; font-weight: 700; transition: all 0.3s; }
        .btn-medical:hover { background: #8bb6c5; transform: translateY(-2px); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-bg">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect x="39" y="8" width="22" height="84" rx="11" fill="#A3C9D6" />
            <rect x="8" y="39" width="84" height="22" rx="11" fill="#A3C9D6" />
            <path d="M50 85 C50 70 52 50 58 30" stroke="#1a1a1a" stroke-width="1" fill="none"/>
        </svg>
    </div>

    <header class="w-full max-w-7xl px-8 py-8 flex justify-between items-center z-50">
        <div class="text-2xl font-extrabold italic tracking-tighter">K-Brain</div>
        <a href="https://lin.ee/your-id" class="px-6 py-2.5 bg-green-500 text-white text-xs font-bold rounded-full hover:bg-green-600 transition">公式LINEでさらに深く</a>
    </header>

    <main class="w-full max-w-5xl px-6 py-12 text-center">
        <h1 class="text-5xl md:text-7xl font-extrabold tracking-tighter mb-6 leading-tight">
            視点が重なるとき、<br>臨床は変わる。
        </h1>
        <p class="text-lg text-slate-400 font-light mb-12">
            リハビリテーションと看護の視点が重なる場所に。<br>
            16万件の学術データから、チーム医療の揺るぎない共通言語を。
        </p>

        <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16 text-left">
            <div class="premium-card p-6 flex items-center space-x-4">
                <div class="w-12 h-12 bg-sky-50 text-sky-500 rounded-full flex items-center justify-center font-bold">#1</div>
                <div>
                    <div class="text-[10px] text-slate-400 uppercase tracking-widest font-bold">収録エビデンス数</div>
                    <div class="text-3xl font-extrabold">168,349+</div>
                </div>
            </div>
            <div class="premium-card p-6 flex items-center space-x-4">
                <div class="w-12 h-12 bg-sky-50 text-sky-500 rounded-full flex items-center justify-center font-bold">#2</div>
                <div>
                    <div class="text-[10px] text-slate-400 uppercase tracking-widest font-bold">対応専門領域</div>
                    <div class="text-3xl font-extrabold">12 Areas</div>
                </div>
            </div>
            <div class="premium-card p-6 flex items-center space-x-4">
                <div class="w-12 h-12 bg-sky-50 text-sky-500 rounded-full flex items-center justify-center font-bold">#3</div>
                <div>
                    <div class="text-[10px] text-slate-400 uppercase tracking-widest font-bold">更新頻度</div>
                    <div class="text-3xl font-extrabold">Weekly</div>
                </div>
            </div>
        </section>

        <div class="max-w-3xl mx-auto search-pill p-2 flex items-center mb-20">
            <form action="/search" method="GET" class="flex w-full items-center">
                <input type="text" name="q" placeholder="疾患・手技・キーワード..." class="flex-grow px-6 py-4 text-lg outline-none bg-transparent">
                <button type="submit" class="btn-medical px-10 py-4 uppercase text-xs tracking-widest">Analyze</button>
            </form>
        </div>

        <div class="w-full h-32 bg-slate-50 border border-dashed border-slate-200 flex items-center justify-center text-slate-300 text-xs mb-20 rounded-xl">
            ADVERTISEMENT SLOT
        </div>

        <section class="text-left mb-20">
            <h2 class="text-3xl font-extrabold mb-10 text-center">HOW TO USE</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="premium-card p-8">
                    <div class="text-sky-500 font-bold mb-4">STEP 01</div>
                    <h3 class="font-bold mb-2">キーワード入力</h3>
                    <p class="text-xs text-slate-500">臨床での疑問（例：心不全 離床）を入力して解析を開始します。</p>
                </div>
                <div class="premium-card p-8">
                    <div class="text-sky-500 font-bold mb-4">STEP 02</div>
                    <h3 class="font-bold mb-2">エビデンス抽出</h3>
                    <p class="text-xs text-slate-500">16万件の知能から、リハと看護の両視点で最適な論文を特定。</p>
                </div>
                <div class="premium-card p-8">
                    <div class="text-sky-500 font-bold mb-4">STEP 03</div>
                    <h3 class="font-bold mb-2">現場での実践</h3>
                    <p class="text-xs text-slate-500">具体的な根拠をチームで共有し、介入の確信へと繋げます。</p>
                </div>
            </div>
        </section>
    </main>

    <footer class="w-full py-12 border-t border-slate-100 text-center bg-white">
        <p class="text-[10px] text-slate-300 tracking-[0.4em] font-bold uppercase">&copy; 2026 K-BRAIN NEXUS PROJECT</p>
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
    if not query: return render_template_string(INDEX_HTML)
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT title, abstract, url FROM papers WHERE title ILIKE %s OR abstract ILIKE %s ORDER BY id DESC LIMIT 30", (f'%{query}%', f'%{query}%'))
        rows = cur.fetchall(); cur.close(); conn.close()
        
        results_html = f'''
        <body style="background:#fafafa; color:#1a1a1a; font-family:sans-serif; padding:40px;">
            <div style="max-width:800px; margin:0 auto;">
                <h2 style="font-weight:800; font-size:24px; margin-bottom:20px;">「{query}」の解析結果</h2>
                {"".join([f'<div style="background:white; padding:30px; border-radius:20px; margin-bottom:20px; border:1px solid #f1f5f9;"><strong>{r[0]}</strong><p style="font-size:14px; color:#666; margin:15px 0;">{r[1] or "詳細は文献を確認してください。"}</p><a href="{r[2]}" target="_blank" style="color:#A3C9D6; text-decoration:none; font-weight:bold;">文献を開く →</a></div>' for r in rows])}
                <div style="text-align:center; margin-top:40px;"><a href="/" style="color:#999; text-decoration:none;">← 戻る</a></div>
            </div>
        </body>
        '''
        return results_html
    except Exception as e: return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
