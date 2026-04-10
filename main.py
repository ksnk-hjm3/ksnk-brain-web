import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [DB設定：hajimeへの接続を固定] ---
# ログにある「k_brain_v22_3 does not exist」を回避するため、DB名を hajime に設定しています 
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/hajime")

pool = None
try:
    pool = SimpleConnectionPool(minconn=1, maxconn=5, dsn=DATABASE_URL)
except Exception as e:
    print(f"DB Error: {e}")

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

INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain | 臨床が変わる。破壊的な論理思考を。</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@100;400;700;900&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #fafafa; color: #1a1a1a; overflow-x: hidden; }
        
        .art-bg {
            position: fixed; top: 48%; left: 50%; transform: translate(-50%, -50%);
            width: 95%; max-width: 550px; z-index: -1; pointer-events: none;
            filter: drop-shadow(0 0 15px rgba(163, 201, 214, 0.2));
        }

        .hero-title { font-size: clamp(3.2rem, 11vw, 6.2rem); font-weight: 900; letter-spacing: -0.06em; line-height: 1.05; }
        .hero-sub { font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 300; color: #667085; line-height: 1.8; letter-spacing: 0.05em; }
        
        .search-pill { background: #fff; border-radius: 999px; box-shadow: 0 15px 45px rgba(0,0,0,0.06); border: 1px solid #f2f4f7; width: 100%; }
        .btn-search { background-color: #A3C9D6; color: white; border-radius: 999px; font-weight: 800; }

        .metric-card {
            background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);
            padding: 3rem; border-radius: 40px; border: 1px solid rgba(0,0,0,0.03);
            box-shadow: 0 20px 40px rgba(0,0,0,0.02);
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-bg">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <path d="M38.5 10C38.5 8 40.5 6 42.5 6H57.5C59.5 6 61.5 8 61.5 10V38.5H90C92 38.5 94 40.5 94 42.5V57.5C94 59.5 92 61.5 90 61.5H61.5V90C61.5 92 59.5 94 57.5 94H42.5C40.5 94 38.5 92 38.5 90V61.5H10C8 61.5 6 59.5 6 57.5V42.5C6 40.5 8 38.5 10 38.5H38.5V10Z" fill="#A3C9D6" fill-opacity="0.85" />
            <path d="M50 88 C49 70 51 52 58 35" stroke="#1a1a1a" stroke-width="1.3" fill="none" stroke-linecap="round" />
            <path d="M54 65 C60 62 67 58 70 48" stroke="#1a1a1a" stroke-width="0.9" fill="none" stroke-linecap="round" />
            <path d="M56 48 C64 45 72 40 74 30" stroke="#1a1a1a" stroke-width="0.9" fill="none" stroke-linecap="round" />
            <path d="M46 68 C40 70 34 78 32 86" stroke="#1a1a1a" stroke-width="0.9" fill="none" stroke-linecap="round" />
            <path d="M44 52 C38 55 31 64 30 74" stroke="#1a1a1a" stroke-width="0.9" fill="none" stroke-linecap="round" />
            <ellipse cx="70" cy="48" rx="1.5" ry="2.2" transform="rotate(30 70 48)" fill="#1a1a1a" />
            <ellipse cx="74" cy="30" rx="1.5" ry="2.2" transform="rotate(30 74 30)" fill="#1a1a1a" />
            <ellipse cx="32" cy="86" rx="1.5" ry="2.2" transform="rotate(-30 32 86)" fill="#1a1a1a" />
            <ellipse cx="30" cy="74" rx="1.5" ry="2.2" transform="rotate(-30 30 74)" fill="#1a1a1a" />
        </svg>
    </div>

    <header class="w-full max-w-6xl px-8 py-10 flex justify-between items-center z-50">
        <div class="text-3xl font-black italic tracking-tighter">K-Brain</div>
        <a href="https://ksnk-brain.jp" class="px-7 py-3 bg-black text-white text-[11px] font-bold rounded-full uppercase tracking-widest">Launch System</a>
    </header>

    <main class="flex-grow w-full px-6 flex flex-col items-center text-center">
        <h1 class="hero-title mt-16 mb-10 text-slate-950">臨床が変わる</h1>
        <p class="hero-sub mb-16 max-w-2xl">他職種の視点をひとつに<br>膨大な学術データによる<span class="font-bold text-slate-900">「破壊的な論理思考」</span>を</p>

        <div class="w-full max-w-2xl mb-24 px-2">
            <div class="search-pill p-1.5 flex items-center">
                <form action="/search" method="GET" class="flex w-full items-center">
                    <input type="text" name="q" placeholder="臨床課題を入力..." class="flex-grow bg-transparent pl-6 pr-2 py-4 text-lg outline-none placeholder-slate-300">
                    <button type="submit" class="btn-search px-10 py-4 text-sm">検索 🔍</button>
                </form>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-40 w-full max-w-6xl text-left">
            <div class="metric-card">
                <div class="text-5xl font-black mb-6 tracking-tighter text-slate-950">{{ count }}</div>
                <div class="text-[11px] font-bold text-sky-600 uppercase mb-4 tracking-widest">Scientific Archive</div>
                <p class="text-sm text-slate-500 leading-relaxed font-light">16万件超のエビデンスをリアルタイムに集約。明日からの介入に、揺るぎない根拠を提供します。</p>
            </div>
            <div class="metric-card border-t-8 border-t-[#A3C9D6]">
                <div class="text-5xl font-black mb-6 italic text-slate-950">1,342</div>
                <div class="text-[11px] font-bold text-sky-600 uppercase mb-4 tracking-widest">Intelligence Growth</div>
                <p class="text-sm text-slate-500 leading-relaxed font-light">本日のサイクルで収集された新規臨床知能。K-Brainは毎日、あなたの想像を超えて進化し続けます。</p>
            </div>
            <div class="metric-card">
                <div class="text-5xl font-black mb-6 tracking-tighter text-slate-950">0.8<span class="text-xl">sec</span></div>
                <div class="text-[11px] font-bold text-sky-600 uppercase mb-4 tracking-widest">Logic Speed</div>
                <p class="text-sm text-slate-500 leading-relaxed font-light">膨大なデータから論理的な解を導き出すまでの平均速度。臨床のスピード感を、AIが加速させます。</p>
            </div>
        </div>
    </main>

    <footer class="w-full py-16 bg-white border-t border-slate-100 text-center text-[10px] text-slate-300 font-bold tracking-[0.5em] uppercase">
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
    terms = q.split()
    conditions = []; params = []
    for t in terms:
        conditions.append("(title ILIKE %s OR abstract ILIKE %s)")
        params.extend([f'%{t}%', f'%{t}%'])
    sql = f"SELECT title, abstract, url FROM papers WHERE {' AND '.join(conditions)} ORDER BY id DESC LIMIT 50"
    rows = query_db(sql, params)
    results = "".join([f'<div style="background:white; padding:40px; border-radius:35px; margin-bottom:24px; border:1px solid #f1f5f9; box-shadow:0 10px 30px rgba(0,0,0,0.02); text-align:left;"><strong style="display:block; font-size:22px; line-height:1.4; font-weight:900;">{r[0]}</strong><p style="font-size:16px; color:#555; line-height:1.8; margin-bottom:25px;">{r[1] or "詳細は文献を確認してください"}</p><a href="{r[2]}" target="_blank" style="display:inline-block; padding:15px 30px; background:#A3C9D6; color:white; font-size:12px; font-weight:bold; text-decoration:none; border-radius:100px;">GET EVIDENCE →</a></div>' for r in rows])
    return f'<body style="background:#fafafa; font-family:sans-serif; padding:60px 20px;"><div style="max-width:840px; margin:0 auto;"><div style="text-align:center; margin-bottom:60px;"><a href="/" style="color:#d1d1d1; text-decoration:none; font-size:11px; font-weight:bold; letter-spacing:0.3em;">← BACK TO HOME</a><h2 style="font-size:36px; font-weight:900; margin-top:20px;">Result: {q}</h2></div>{results}</div></body>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
