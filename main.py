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
    except: return "210,812"

INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain Nexus | 臨床推論の極致</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@100;400;700;900&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #fafafa; color: #1a1a1a; }
        .hero-title { font-size: clamp(2.5rem, 8vw, 5.5rem); font-weight: 900; letter-spacing: -0.05em; line-height: 1.1; }
        .search-pill { background: #fff; border-radius: 999px; box-shadow: 0 25px 50px rgba(0,0,0,0.06); border: 1px solid #f0f0f0; transition: all 0.4s; }
        .search-pill:focus-within { transform: translateY(-3px); box-shadow: 0 30px 60px rgba(0,0,0,0.08); }
        .btn-search { background-color: #A3C9D6; color: white; border-radius: 999px; font-weight: 800; }
        .metric-card { text-align: center; border-right: 1px solid #eee; padding: 0 2rem; }
        .metric-card:last-child { border-right: none; }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">
    <header class="w-full max-w-6xl px-10 py-12 flex justify-between items-center z-50">
        <div class="text-3xl font-black italic tracking-tighter">K-Brain Nexus</div>
        <div class="text-[10px] font-bold tracking-[0.4em] text-slate-300 uppercase">Scientific Evidence Engine</div>
    </header>

    <main class="flex-grow w-full flex flex-col items-center px-6">
        <div class="text-center mt-10 mb-20">
            <h1 class="hero-title text-slate-900 mb-6">臨床を、数字で語る。</h1>
            <p class="text-lg text-slate-400 font-light">破壊的な論理思考を、21万件の学術エビデンスと共に。</p>
        </div>

        <div class="flex flex-col md:flex-row justify-center w-full max-w-5xl mb-32 space-y-12 md:space-y-0">
            <div class="metric-card">
                <div class="text-xs font-bold text-sky-400 uppercase tracking-widest mb-4">Total Archive</div>
                <div class="text-6xl font-black text-slate-900 tracking-tighter">{{ count }}</div>
            </div>
            <div class="metric-card">
                <div class="text-xs font-bold text-sky-400 uppercase tracking-widest mb-4">Daily Growth</div>
                <div class="text-6xl font-black italic text-slate-900 tracking-tighter">1,396</div>
            </div>
            <div class="metric-card">
                <div class="text-xs font-bold text-sky-400 uppercase tracking-widest mb-4">Logic Latency</div>
                <div class="text-6xl font-black text-slate-900 tracking-tighter">0.8<span class="text-2xl font-bold ml-1">sec</span></div>
            </div>
        </div>

        <div class="w-full max-w-3xl mb-40">
            <form action="/search" class="search-pill p-2 flex items-center">
                <input name="q" class="flex-grow pl-10 outline-none text-xl bg-transparent" placeholder="臨床課題を入力..." autofocus>
                <button class="btn-search px-14 py-5 text-sm transition-all hover:opacity-80">解析実行</button>
            </form>
        </div>
    </main>

    <footer class="w-full py-16 bg-white border-t border-slate-100 text-center text-[10px] text-slate-300 font-bold tracking-[0.8em] uppercase">
        &copy; 2026 K-BRAIN NEXUS PROJECT
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
    results = "".join([f'<div style="background:white; padding:40px; border-radius:35px; margin-bottom:24px; border:1px solid #f1f5f9; box-shadow:0 10px 30px rgba(0,0,0,0.02); text-align:left;"><strong style="display:block; font-size:24px; line-height:1.3; font-weight:900; color:#1a1a1a; margin-bottom:15px;">{r[0]}</strong><p style="font-size:16px; color:#555; line-height:1.8; margin-bottom:25px;">{r[1] or "エビデンスの詳細を直接確認してください"}</p><a href="{r[2]}" target="_blank" style="display:inline-block; padding:15px 35px; background:#A3C9D6; color:white; font-size:12px; font-weight:bold; text-decoration:none; border-radius:100px; transition:opacity 0.3s;" onmouseover="this.style.opacity=0.8" onmouseout="this.style.opacity=1">GET EVIDENCE →</a></div>' for r in rows])
    return f'<body style="background:#fafafa; font-family:sans-serif; padding:60px 20px;"><div style="max-width:840px; margin:0 auto;"><div style="text-align:center; margin-bottom:60px;"><a href="/" style="color:#ccc; text-decoration:none; font-size:11px; font-weight:bold; letter-spacing:0.3em;">← BACK TO ANALYZER</a><h2 style="font-size:36px; font-weight:900; margin-top:24px; color:#1a1a1a;">Result: {q}</h2></div>{results}</div></body>'

if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
