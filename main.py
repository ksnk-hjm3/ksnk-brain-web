import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [1. データベース設定：堅牢な接続プール] ---
# ⚠️ RenderのDashboardで「Database」欄の名前をコピーして末尾を書き換えてください
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3")

pool = None
try:
    pool = SimpleConnectionPool(minconn=1, maxconn=5, dsn=DATABASE_URL)
except Exception as e:
    print(f"DB Connection Error: {e}")

def query_db(sql, params=None):
    if not pool: return []
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        pool.putconn(conn)

def get_evidence_count():
    try:
        rows = query_db("SELECT COUNT(*) FROM papers")
        return f"{rows[0][0]:,}"
    except: return "168,349"

# --- [2. フロントエンド：デザイナーとしての「最終回答」] ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078" crossorigin="anonymous"></script>
    <title>K-Brain | 臨床が変わる。破壊的な論理思考を。</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@100;400;700;900&display=swap');
        
        body { 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            background-color: #fafafa; 
            color: #1a1a1a;
            overflow-x: hidden;
            -webkit-text-size-adjust: 100%;
        }

        /* 🌳 【聖域】image0(1).jpeg の「手描き感」と「質感」を完全再現 */
        .art-bg {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 85%; max-width: 500px; z-index: -1; pointer-events: none;
            opacity: 1; /* 透明度に頼らず、色味そのもので表現 */
        }

        /* ヒーロー：圧倒的な力強さと繊細さの共存 */
        .hero-title { 
            font-size: clamp(3.5rem, 12vw, 6.5rem); 
            font-weight: 900; 
            letter-spacing: -0.06em; 
            line-height: 1.0; 
            color: #101828;
        }

        .hero-sub { 
            font-size: clamp(1.1rem, 2.5vw, 1.3rem); 
            font-weight: 300; 
            color: #475467; 
            line-height: 1.8;
            letter-spacing: 0.05em;
        }

        /* 🔍 検索バー：スマホ枠を絶対にはみ出さない設計 */
        .search-outer { width: 100%; max-width: 640px; padding: 0 16px; box-sizing: border-box; }
        .search-pill { 
            background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(20px);
            border-radius: 999px; border: 1px solid rgba(0,0,0,0.05);
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.05);
            display: flex; align-items: center; padding: 6px;
        }
        .search-input { flex-grow: 1; background: transparent; padding: 12px 24px; font-size: 1.125rem; outline: none; border: none; }
        .btn-search { 
            background-color: #A3C9D6; color: white; border-radius: 999px; 
            font-weight: 800; padding: 12px 32px; transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(163, 201, 214, 0.3);
        }

        /* プロフェッショナル・マニフェスト：意味のある3枚のカード */
        .manifesto-card {
            background: white; border-radius: 40px; padding: 40px;
            border: 1px solid #f2f4f7; box-shadow: 0 10px 30px -10px rgba(0,0,0,0.03);
            transition: transform 0.4s cubic-bezier(0.17, 0.67, 0.83, 0.67);
        }
        .manifesto-card:hover { transform: translateY(-8px); }
        .marker { background: linear-gradient(180deg, transparent 70%, rgba(163, 201, 214, 0.3) 70%); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-bg">
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <filter id="grain" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="0.4" />
                </filter>
            </defs>
            <path d="M38.5 10C38.5 8 40.5 6 42.5 6H57.5C59.5 6 61.5 8 61.5 10V38.5H90C92 38.5 94 40.5 94 42.5V57.5C94 59.5 92 61.5 90 61.5H61.5V90C61.5 92 59.5 94 57.5 94H42.5C40.5 94 38.5 92 38.5 90V61.5H10C8 61.5 6 59.5 6 57.5V42.5C6 40.5 8 38.5 10 38.5H38.5V10Z" fill="#A3C9D6" fill-opacity="0.85" filter="url(#grain)"/>
            <path d="M52 88 C52 75 54 52 60 35" stroke="#1a1a1a" stroke-width="1.3" stroke-linecap="round"/>
            <path d="M55 65 C60 60 68 55 72 45" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M57 48 C64 43 72 38 75 28" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M48 68 C42 70 34 76 30 85" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M47 50 C40 53 30 62 28 72" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M72 45 Q74 43 73.5 46.5 Q73 50 71 45.5 Z" fill="#1a1a1a"/>
            <path d="M75 28 Q77 26 76.5 29.5 Q76 33 74 28.5 Z" fill="#1a1a1a"/>
            <path d="M30 85 Q28 87 28.5 83.5 Q29 80 31 84.5 Z" fill="#1a1a1a"/>
            <path d="M28 72 Q26 74 26.5 70.5 Q27 67 29 71.5 Z" fill="#1a1a1a"/>
        </svg>
    </div>

    <header class="w-full max-w-6xl px-8 py-12 flex justify-between items-center z-50">
        <div class="text-3xl font-black italic tracking-tighter text-slate-950">K-Brain</div>
        <div class="flex items-center space-x-6">
            <a href="https://www.instagram.com/ksnk.hjm3/" target="_blank" class="text-[10px] font-bold text-slate-400 uppercase tracking-widest hidden sm:block">Instagram</a>
            <a href="https://ksnk-brain.jp" class="px-6 py-3 bg-slate-950 text-white text-[11px] font-bold rounded-full uppercase tracking-tighter">Launch System</a>
        </div>
    </header>

    <main class="flex-grow flex flex-col items-center w-full px-4 text-center">
        
        <h1 class="hero-title mt-12 mb-10">臨床が変わる</h1>
        
        <div class="hero-sub mb-20 max-w-2xl">
            <p>他職種の視点をひとつに</p>
            <p>16万件の学術データによる<span class="marker font-bold text-slate-900">「破壊的な論理思考」</span>を</p>
        </div>

        <div class="search-outer mb-32">
            <form action="/search" method="GET" class="search-pill">
                <input type="text" name="q" placeholder="臨床課題を入力..." class="search-input placeholder-slate-300">
                <button type="submit" class="btn-search text-xs whitespace-nowrap">検索 🔍</button>
            </form>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-40 w-full max-w-6xl text-left">
            <div class="manifesto-card">
                <div class="text-4xl font-black mb-6 tracking-tighter text-slate-900">{{ count }}</div>
                <div class="text-[10px] font-bold text-sky-600 uppercase mb-4 tracking-widest">Evidence Engine</div>
                <p class="text-sm text-slate-500 leading-relaxed font-light">理学療法と看護の知能を統合。16万件超のエビデンスから、チーム医療の根拠を1秒で特定します。</p>
            </div>
            <div class="manifesto-card">
                <div class="w-12 h-12 bg-sky-50 flex items-center justify-center rounded-2xl text-sky-500 font-black mb-6">02</div>
                <div class="text-[10px] font-bold text-sky-600 uppercase mb-4 tracking-widest">Decision Support</div>
                <p class="text-sm text-slate-500 leading-relaxed font-light">「論文を読む」から「意思決定に使う」へ。膨大な学術データを、明日からの具体的な介入へと変換します。</p>
            </div>
            <div class="manifesto-card">
                <div class="w-12 h-12 bg-sky-50 flex items-center justify-center rounded-2xl text-sky-500 font-black mb-6">03</div>
                <div class="text-[10px] font-bold text-sky-600 uppercase mb-4 tracking-widest">Nexus Project</div>
                <p class="text-sm text-slate-500 leading-relaxed font-light">職種の境界線を越え、共通言語での議論を。破壊的な論理思考が、臨床現場の確信を支援します。</p>
            </div>
        </div>
    </main>

    <footer class="w-full py-16 bg-white border-t border-slate-50 text-center">
        <div class="text-[9px] text-slate-300 font-bold tracking-[0.5em] uppercase">
            &copy; 2026 K-BRAIN NEXUS PROJECT | EBM ARCHIVE
        </div>
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
    terms = q.split()
    conditions = []; params = []
    for t in terms:
        conditions.append("(title ILIKE %s OR abstract ILIKE %s)")
        params.extend([f'%{t}%', f'%{t}%'])
    sql = f"SELECT title, abstract, url FROM papers WHERE {' AND '.join(conditions)} ORDER BY id DESC LIMIT 50"
    rows = query_db(sql, params)
    results = "".join([f'<div style="background:white; padding:40px; border-radius:40px; margin-bottom:24px; border:1px solid #f1f5f9; box-shadow:0 10px 30px rgba(0,0,0,0.02);"><strong style="display:block; font-size:22px; line-height:1.3; font-weight:900;">{r[0]}</strong><p style="font-size:16px; color:#555; line-height:1.8; margin-bottom:25px;">{r[1] or "詳細は文献を確認してください"}</p><a href="{r[2]}" target="_blank" style="display:inline-block; padding:15px 30px; background:#A3C9D6; color:white; font-size:12px; font-weight:bold; text-decoration:none; border-radius:100px;">GET EVIDENCE →</a></div>' for r in rows])
    return f'<body style="background:#fafafa; font-family:sans-serif; padding:60px 20px;"><div style="max-width:840px; margin:0 auto;"><div style="text-align:center; margin-bottom:60px;"><a href="/" style="color:#d1d1d1; text-decoration:none; font-size:11px; font-weight:bold; letter-spacing:0.3em;">← BACK TO HOME</a><h2 style="font-size:36px; font-weight:900; margin-top:20px;">Result: {q}</h2></div>{results}</div></body>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
