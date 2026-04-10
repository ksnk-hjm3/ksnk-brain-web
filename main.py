import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from flask import Flask, request, render_template_string

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/ksnk_brain")

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
    except: return "0"

INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain Nexus | 臨床知能</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@300;700;900&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #fafafa; color: #1a1a1a; }
        .hero-title { font-size: clamp(3rem, 8vw, 5.5rem); font-weight: 900; letter-spacing: -0.04em; }
        .search-container { max-width: 800px; width: 100%; margin: 0 auto; }
        .search-pill { background: #fff; border-radius: 999px; box-shadow: 0 20px 60px rgba(0,0,0,0.05); border: 1px solid #eee; }
        .btn-search { background-color: #A3C9D6; color: white; border-radius: 999px; font-weight: 700; transition: all 0.3s; }
        .btn-search:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(163, 201, 214, 0.3); }
        .metric-label { font-size: 10px; font-weight: 900; color: #A3C9D6; letter-spacing: 0.2em; text-transform: uppercase; }
        .metric-value { font-size: 3.5rem; font-weight: 900; line-height: 1; letter-spacing: -0.05em; color: #1a1a1a; }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">
    <header class="w-full max-w-6xl px-10 py-12 flex justify-between items-center">
        <div class="text-2xl font-black italic tracking-tighter">K-Brain Nexus</div>
        <div class="text-[10px] font-bold tracking-widest text-slate-300 uppercase">Scientific Clinical Intelligence</div>
    </header>

    <main class="flex-grow w-full flex flex-col items-center px-6">
        <div class="text-center mb-16">
            <h1 class="hero-title mb-4">臨床を、数字で語る。</h1>
            <p class="text-slate-400 font-light tracking-wide">20万件超のエビデンスが、あなたの判断を破壊的な論理へと変える。</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-12 w-full max-w-5xl mb-24">
            <div class="text-center border-b md:border-b-0 md:border-r border-slate-100 pb-8 md:pb-0">
                <div class="metric-label mb-3">Total Evidence</div>
                <div class="metric-value">{{ count }}</div>
            </div>
            <div class="text-center border-b md:border-b-0 md:border-r border-slate-100 pb-8 md:pb-0">
                <div class="metric-label mb-3">Today's Growth</div>
                <div class="metric-value italic">1,398</div>
            </div>
            <div class="text-center">
                <div class="metric-label mb-3">Processing Speed</div>
                <div class="metric-value">0.8<span class="text-xl">sec</span></div>
            </div>
        </div>

        <div class="search-container">
            <form action="/search" class="search-pill p-2 flex items-center">
                <input name="q" class="flex-grow pl-8 outline-none text-lg bg-transparent" placeholder="疾患、介入、臨床課題を解析...">
                <button class="btn-search px-12 py-4">解析を開始</button>
            </form>
        </div>
    </main>

    <footer class="w-full py-20 text-center border-t border-slate-50 mt-20">
        <p class="text-[10px] font-bold text-slate-200 tracking-[1em] uppercase">&copy; 2026 K-BRAIN NEXUS PROJECT</p>
    </footer>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(INDEX_HTML, count=get_evidence_count())

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if not q: return index()
    rows = query_db("SELECT title, abstract, url FROM papers WHERE title ILIKE %s OR abstract ILIKE %s LIMIT 50", (f'%{q}%', f'%{q}%'))
    results = "".join([f'<div style="background:white; padding:40px; border-radius:30px; margin-bottom:24px; border:1px solid #f1f5f9; box-shadow:0 10px 30px rgba(0,0,0,0.02); text-align:left;"><strong style="display:block; font-size:22px; line-height:1.3; font-weight:900; color:#1a1a1a; margin-bottom:15px;">{r[0]}</strong><p style="font-size:16px; color:#666; line-height:1.8; margin-bottom:25px;">{r[1] or "エビデンスを直接確認してください"}</p><a href="{r[2]}" target="_blank" style="display:inline-block; color:#A3C9D6; font-weight:bold; text-decoration:none; font-size:14px; letter-spacing:0.1em;">VIEW SOURCE →</a></div>' for r in rows])
    return f'<body style="background:#fafafa; font-family:sans-serif; padding:60px 20px;"><div style="max-width:840px; margin:0 auto;"><a href="/" style="color:#ccc; text-decoration:none; font-size:11px; font-weight:bold; letter-spacing:0.1em;">← BACK TO ANALYZER</a><h2 style="font-size:32px; font-weight:900; margin:40px 0 30px;">Result: {q}</h2>{results}</div></body>'

if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
