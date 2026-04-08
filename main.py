import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [設定エリア] ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# --- [デザイン：Medical Grey & Watermark] ---
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
        
        body { 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            background-color: #f1f5f9; /* 洗練されたライトグレー (Slate-100) */
            color: #1e293b; 
            position: relative;
            overflow-x: hidden;
        }

        /* クスノキの透かし（ウォーターマーク） */
        .watermark {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;
            max-width: 600px;
            opacity: 0.04; /* 極限まで薄くして「気配」を出す */
            z-index: -1;
            pointer-events: none;
        }

        .glass-card { 
            background: rgba(255, 255, 255, 0.7); 
            backdrop-filter: blur(10px); 
            border: 1px solid rgba(203, 213, 225, 0.5); 
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); 
        }

        .search-input:focus { 
            outline: none; 
            border-color: #0ea5e9; 
            box-shadow: 0 0 15px rgba(14, 165, 233, 0.15); 
        }

        .tag-btn { 
            transition: all 0.2s ease; 
            background: #ffffff; 
            border: 1px solid #cbd5e1; 
            cursor: pointer; 
            color: #64748b; 
        }

        .tag-btn:hover { 
            background: #f8fafc; 
            border-color: #0ea5e9; 
            color: #0ea5e9; 
            transform: translateY(-1px); 
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center p-4">

    <svg class="watermark" viewBox="0 0 100 100" fill="currentColor">
        <path d="M50 10 C35 10 25 25 25 45 C25 65 40 70 45 85 L55 85 C60 70 75 65 75 45 C75 25 65 10 50 10 Z M45 40 Q50 35 55 40 M42 50 Q50 45 58 50 M45 60 Q50 55 55 60" fill="none" stroke="currentColor" stroke-width="2"/>
        <path d="M50 10 Q55 5 60 10 M50 15 Q40 10 35 15 M40 30 Q30 25 25 35" fill="none" stroke="currentColor" stroke-width="1.5"/>
    </svg>

    <div class="fixed top-6 right-6 flex items-center space-x-4 text-[10px] tracking-widest text-slate-400 uppercase">
        <div class="flex items-center"><span class="w-2 h-2 bg-sky-500 rounded-full animate-pulse mr-2"></span>Node: Active</div>
        <div class="border-l border-slate-200 pl-4 text-slate-500">Evidence: 168,367</div>
    </div>

    <main class="w-full max-w-3xl text-center space-y-12">
        <header class="space-y-4">
            <h1 class="text-6xl font-extrabold tracking-tighter text-slate-800 italic">K-Brain</h1>
            <div class="space-y-2">
                <p class="text-xl md:text-2xl font-medium text-slate-600">視点が重なるとき、臨床は変わる。</p>
                <p class="text-sm md:text-base text-slate-400 font-light tracking-wide">
                    リハビリテーションと看護の知能を統合。<br>16万件のエビデンスから、チーム医療の「根拠」を1秒で。
                </p>
            </div>
        </header>

        <section class="space-y-6">
            <form action="/search" method="GET" class="relative">
                <input type="text" name="q" placeholder="キーワードを入力してください..." class="search-input w-full p-5 bg-white rounded-xl glass-card text-lg font-light text-slate-700 transition-all">
                <button type="submit" class="absolute right-4 top-4 text-sky-500 hover:text-sky-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                </button>
            </form>
            <div class="flex flex-wrap justify-center gap-3">
                <button onclick="location.href='/search?q=心不全リハ'" class="tag-btn px-4 py-1.5 rounded-full text-xs font-medium">心不全リハ</button>
                <button onclick="location.href='/search?q=夜間せん妄'" class="tag-btn px-4 py-1.5 rounded-full text-xs font-medium">夜間せん妄</button>
                <button onclick="location.href='/search?q=BPSD対応'" class="tag-btn px-4 py-1.5 rounded-full text-xs font-medium">BPSD対応</button>
                <button onclick="location.href='/search?q=フレイル予防'" class="tag-btn px-4 py-1.5 rounded-full text-xs font-medium">フレイル予防</button>
            </div>
        </section>

        <section class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-8 border-t border-slate-200">
            <div class="space-y-1"><div class="text-slate-800 font-bold">Search</div><p class="text-[10px] text-slate-400">臨床の悩みをキーワード検索</p></div>
            <div class="space-y-1"><div class="text-slate-800 font-bold">Analyze</div><p class="text-[10px] text-slate-400">リハと看護、双方の視点で抽出</p></div>
            <div class="space-y-1"><div class="text-slate-800 font-bold">Connect</div><p class="text-[10px] text-slate-500">共通の根拠でチーム医療を強化</p></div>
        </section>
    </main>

    <footer class="fixed bottom-8 text-[10px] text-slate-400 tracking-widest">
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
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
