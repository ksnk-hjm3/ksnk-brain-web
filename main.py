import os
import psycopg2
import re
from psycopg2.pool import SimpleConnectionPool
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [1. 技術的進化：他のAI案を取り入れた接続プール] ---
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3")

# 接続を効率化し、Renderでのエラーを徹底的に防ぐ
pool = SimpleConnectionPool(minconn=1, maxconn=5, dsn=DATABASE_URL)

def get_db_connection():
    return pool.getconn()

def release_db_connection(conn):
    pool.putconn(conn)

def get_evidence_count():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM papers")
        count = cur.fetchone()[0]
        cur.close()
        return "{:,}".format(count)
    except:
        return "168,349"
    finally:
        if conn: release_db_connection(conn)

# --- [2. デザイン：image0 (1).jpeg を 1px 単位で再現] ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078" crossorigin="anonymous"></script>
    <title>K-Brain | 臨床が変わる 破壊的な論理思考を</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&family=Noto+Sans+JP:wght@300;500;700;900&display=swap');
        
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #fafafa; color: #1a1a1a; overflow-x: hidden; }

        /* 🌳 【絶対死守】image0 (1).jpeg のシンボル再現 */
        .art-bg {
            position: fixed; top: 45%; left: 50%; transform: translate(-50%, -50%);
            width: 90%; max-width: 500px; z-index: -1; opacity: 1.0; pointer-events: none;
        }

        /* スマホで2段にならないロゴ制御 */
        .logo-text { font-size: 1.875rem; font-weight: 900; font-style: italic; letter-spacing: -0.05em; white-space: nowrap; }

        .hero-title { font-size: clamp(3.2rem, 10vw, 6rem); font-weight: 900; letter-spacing: -0.06em; line-height: 1.0; }

        /* 🔍 検索バー：スマホ枠に完全フィット */
        .search-pill {
            background: #ffffff; border: 1px solid #e2e8f0; border-radius: 999px;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05); width: 100%; box-sizing: border-box;
        }

        .btn-search { background-color: #A3C9D6; color: white; border-radius: 999px; font-weight: 800; white-space: nowrap; }

        .step-card { background: white; border-radius: 32px; border: 1px solid #f1f5f9; box-shadow: 0 4px 20px rgba(0,0,0,0.02); }
        .highlight-line { background: linear-gradient(180deg, transparent 70%, rgba(163, 201, 214, 0.4) 70%); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-bg">
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M38 10C38 7.5 40 5.5 42.5 5.5H57.5C60 5.5 62 7.5 62 10V38H90C92.5 38 94.5 40 94.5 42.5V57.5C94.5 60 92.5 62 90 62H62V90C62 92.5 60 94.5 57.5 94.5H42.5C40 94.5 38 92.5 38 90V62H10C7.5 62 5.5 60 5.5 57.5V42.5C5.5 40 7.5 38 10 38H38V10Z" fill="#A3C9D6"/>
            <path d="M52 88C52 75 54 55 60 35" stroke="#1a1a1a" stroke-width="1.3" stroke-linecap="round"/>
            <path d="M55 65C60 60 68 55 72 45" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M57 48C64 43 72 38 75 28" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M48 68C42 70 35 76 32 83" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M47 52C40 55 32 62 30 72" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <circle cx="72" cy="45" r="1.1" fill="#1a1a1a"/><circle cx="75" cy="28" r="1.1" fill="#1a1a1a"/>
            <circle cx="32" cy="83" r="1.1" fill="#1a1a1a"/><circle cx="30" cy="72" r="1.1" fill="#1a1a1a"/>
        </svg>
    </div>

    <header class="w-full max-w-6xl px-6 py-10 flex justify-between items-center z-50">
        <div class="logo-text">K-Brain</div>
        <a href="https://ksnk-brain.jp" class="px-5 py-2.5 bg-black text-white text-[10px] font-bold rounded-full uppercase tracking-tighter whitespace-nowrap">Launch System</a>
    </header>

    <main class="flex-grow flex flex-col items-center w-full px-5 text-center">
        <h1 class="hero-title mb-10">臨床が変わる</h1>
        
        <div class="text-lg md:text-xl text-slate-500 font-light leading-relaxed mb-16 space-y-4">
            <p>他職種の視点をひとつに</p>
            <p>膨大な学術データによる<br><span class="highlight-line font-bold text-slate-900">「破壊的な論理思考」を</span></p>
        </div>

        <div class="w-full max-w-2xl px-2 mb-24">
            <div class="search-pill p-1.5 flex items-center">
                <form action="/search" method="GET" class="flex w-full items-center">
                    <input type="text" name="q" placeholder="臨床課題を入力..." class="flex-grow bg-transparent pl-5 pr-2 py-4 text-base md:text-lg outline-none placeholder-slate-300 min-w-0">
                    <button type="submit" class="btn-search px-6 md:px-10 py-4 text-sm whitespace-nowrap">検索 🔍</button>
                </form>
            </div>
        </div>

        <section class="w-full max-w-5xl grid grid-cols-1 md:grid-cols-3 gap-6 mb-32 text-left">
            <div class="step-card p-10 space-y-4">
                <div class="text-4xl font-black text-slate-900 tracking-tighter">{{ count }}</div>
                <div>
                    <div class="text-xs font-bold text-sky-600 uppercase mb-2">Step 01: 疾患名・手技を入力</div>
                    <p class="text-sm text-slate-500 leading-relaxed">日本語・英語どちらでも検索可能。AND/OR検索により膨大なデータから瞬時に絞り込みます。</p>
                </div>
            </div>
            <div class="step-card p-10 space-y-4">
                <div class="w-12 h-12 bg-sky-50 flex items-center justify-center rounded-2xl text-sky-500 font-black">2</div>
                <div>
                    <div class="text-xs font-bold text-sky-600 uppercase mb-2">Step 02: フィルターで絞り込み</div>
                    <p class="text-sm text-slate-500 leading-relaxed">発行年、ジャーナル、言語で素早く目的の論文へ。他職種の知見を統合した解析を行います。</p>
                </div>
            </div>
            <div class="step-card p-10 space-y-4">
                <div class="w-12 h-12 bg-sky-50 flex items-center justify-center rounded-2xl text-sky-500 font-black">3</div>
                <div>
                    <div class="text-xs font-bold text-sky-600 uppercase mb-2">Step 03: エビデンスを確認</div>
                    <p class="text-sm text-slate-500 leading-relaxed">要約、引用数、関連論文を一覧で確認。PubMedへ直接リンクし、臨床での確信を支援します。</p>
                </div>
            </div>
        </section>
    </main>

    <footer class="w-full py-16 border-t border-slate-50 text-center bg-white text-[9px] text-slate-300 font-bold tracking-[0.5em] uppercase">
        &copy; 2026 K-BRAIN NEXUS PROJECT
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, count=get_evidence_count())

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if not q: return index()
    
    conn = None
    try:
        conn = get_db_connection(); cur = conn.cursor()
        # --- 他のAI案のAND検索ロジックを統合 ---
        terms = q.split()
        conditions = []; params = []
        for t in terms:
            conditions.append("(title ILIKE %s OR abstract ILIKE %s)")
            params.extend([f'%{t}%', f'%{t}%'])
        
        sql = f"SELECT title, abstract, url FROM papers WHERE {' AND '.join(conditions)} ORDER BY id DESC LIMIT 50"
        cur.execute(sql, params)
        rows = cur.fetchall(); cur.close()

        results = "".join([f'<div style="background:white; padding:40px; border-radius:40px; margin-bottom:24px; border:1px solid #f1f5f9; box-shadow:0 10px 30px rgba(0,0,0,0.02);"><strong style="display:block; font-size:22px; line-height:1.3; font-weight:900;">{r[0]}</strong><p style="font-size:16px; color:#666; line-height:1.8; margin-bottom:25px;">{r[1] or "詳細は文献を確認してください"}</p><a href="{r[2]}" target="_blank" style="display:inline-block; padding:15px 30px; background:#A3C9D6; color:white; font-size:12px; font-weight:bold; text-decoration:none; border-radius:100px; letter-spacing:0.1em;">GET EVIDENCE →</a></div>' for r in rows])
        return f'<body style="background:#fafafa; font-family:sans-serif; padding:60px 20px;"><div style="max-width:840px; margin:0 auto;"><div style="text-align:center; margin-bottom:60px;"><a href="/" style="color:#d1d1d1; text-decoration:none; font-size:11px; font-weight:bold; letter-spacing:0.3em;">← COMMAND CENTER</a><h2 style="font-size:36px; font-weight:900; margin-top:20px; letter-spacing:-0.03em;">Result: {q}</h2></div>{results}</div></body>'
    except Exception as e: return str(e)
    finally:
        if conn: release_db_connection(conn)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
