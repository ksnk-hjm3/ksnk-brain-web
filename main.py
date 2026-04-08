import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [設定エリア] ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# --- [デザイン：Readdy AI / Premium Grey Edition] ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078" crossorigin="anonymous"></script>
    <title>K-Brain | 臨床知能アーカイブ</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Noto+Sans+JP:wght@300;400;700&display=swap');
        
        body { 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            background-color: #f8fafc; /* より明るく清潔感のあるグレー */
            color: #0f172a;
        }

        /* クスノキの透かし（巨大なアイコンを背景に配置） */
        .bg-watermark {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 100%;
            max-width: 800px;
            opacity: 0.02;
            z-index: -1;
            pointer-events: none;
        }

        /* Readdy風：浮遊感のあるガラスカード */
        .premium-card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.03), 0 0 0 1px rgba(0, 0, 0, 0.01);
            border-radius: 2.5rem;
        }

        /* 検索バーのカスタムシャドウ */
        .search-container {
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);
            border: 1px solid rgba(226, 232, 240, 0.8);
        }

        .hero-text {
            letter-spacing: -0.05em;
            line-height: 1.1;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <svg class="bg-watermark" viewBox="0 0 100 100" fill="currentColor">
        <path d="M50 10 C35 10 25 25 25 45 C25 65 40 70 45 85 L55 85 C60 70 75 65 75 45 C75 25 65 10 50 10 Z" fill="none" stroke="currentColor" stroke-width="0.5"/>
    </svg>

    <header class="w-full max-w-6xl px-6 py-8 flex justify-between items-center z-50">
        <div class="text-2xl font-extrabold italic tracking-tighter text-slate-900">K-Brain</div>
        <div class="flex items-center space-x-6">
            <a href="https://www.instagram.com/ksnk.hjm3/" target="_blank" class="text-xs font-bold text-slate-400 hover:text-sky-500 uppercase tracking-widest transition">Instagram</a>
            <a href="https://ksnk-brain.jp" class="px-6 py-2.5 bg-slate-900 text-white text-xs font-bold rounded-full hover:bg-sky-600 transition shadow-lg shadow-slate-200">検索エンジン起動</a>
        </div>
    </header>

    <main class="w-full max-w-4xl px-6 py-20 text-center flex flex-col items-center">
        <div class="inline-block px-4 py-1 mb-8 bg-sky-50 text-sky-600 rounded-full text-[10px] font-bold uppercase tracking-widest border border-sky-100">
            Nexus Project v22.3
        </div>
        
        <h1 class="hero-text text-6xl md:text-8xl font-extrabold text-slate-900 mb-8">
            視点が重なるとき、<br><span class="text-transparent bg-clip-text bg-gradient-to-r from-slate-900 to-slate-500">臨床は変わる。</span>
        </h1>
        
        <p class="text-lg md:text-xl text-slate-500 font-light mb-16 leading-relaxed max-w-2xl">
            理学療法と看護の知能を統合。16万件のエビデンスから、<br class="hidden md:block">
            チーム医療の「根拠」を1秒で。
        </p>

        <div class="w-full max-w-2xl premium-card p-2 mb-12">
            <form action="/search" method="GET" class="flex items-center">
                <input type="text" name="q" placeholder="心不全 離床 基準..." 
                       class="flex-grow bg-transparent px-6 py-5 text-lg focus:outline-none placeholder-slate-300">
                <button type="submit" class="mr-2 px-8 py-4 bg-sky-500 text-white rounded-[1.8rem] font-bold hover:bg-sky-600 transition shadow-md shadow-sky-100">
                    ANALYZE
                </button>
            </form>
        </div>

        <div class="flex flex-wrap justify-center gap-3">
            <span class="w-full text-[10px] text-slate-400 uppercase tracking-widest mb-2 font-bold">Trending Intelligence</span>
            <button onclick="location.href='/search?q=心不全リハ'" class="px-5 py-2 bg-white border border-slate-100 rounded-full text-xs text-slate-400 hover:text-sky-500 hover:border-sky-200 transition shadow-sm">心不全リハ</button>
            <button onclick="location.href='/search?q=夜間せん妄'" class="px-5 py-2 bg-white border border-slate-100 rounded-full text-xs text-slate-400 hover:text-sky-500 hover:border-sky-200 transition shadow-sm">夜間せん妄</button>
            <button onclick="location.href='/search?q=BPSD対応'" class="px-5 py-2 bg-white border border-slate-100 rounded-full text-xs text-slate-400 hover:text-sky-500 hover:border-sky-200 transition shadow-sm">BPSD対応</button>
        </div>
    </main>

    <footer class="mt-auto py-12 text-[10px] text-slate-300 tracking-widest font-bold uppercase">
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

        # 結果画面もReaddy AI風に
        results_html = f'''
        <body style="background:#f8fafc; color:#0f172a; font-family:sans-serif; padding:40px;">
            <div style="max-width:800px; margin:0 auto;">
                <header style="margin-bottom:40px;">
                    <a href="/" style="text-decoration:none; color:#64748b; font-size:12px; font-weight:bold; letter-spacing:0.1em; text-transform:uppercase;">← Back to Home</a>
                    <h2 style="font-size:32px; font-weight:800; margin-top:16px;">Search Results for <span style="color:#0ea5e9;">"{query}"</span></h2>
                    <p style="color:#94a3b8; font-size:14px;">{len(rows)} cases identified in clinical database.</p>
                </header>
                {"".join([f'<div style="background:white; padding:32px; border-radius:24px; margin-bottom:24px; border:1px solid #f1f5f9; box-shadow:0 10px 15px -3px rgba(0,0,0,0.02);"> <strong style="display:block; font-size:18px; line-height:1.4; margin-bottom:12px;">{r[0]}</strong> <p style="font-size:14px; color:#475569; line-height:1.6; margin-bottom:20px;">{r[1] or "詳細データは外部リンクを確認してください。"}</p> <a href="{r[2]}" target="_blank" style="display:inline-block; color:#0ea5e9; font-size:12px; font-weight:bold; text-decoration:none; border-bottom:2px solid #e0f2fe;">[文献エビデンスを開く]</a> </div>' for r in rows])}
            </div>
        </body>
        '''
        return results_html
    except Exception as e:
        return f"Database Connection Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
