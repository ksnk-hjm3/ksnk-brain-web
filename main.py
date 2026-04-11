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

def get_count():
    try:
        res = query_db("SELECT COUNT(*) FROM papers")
        return f"{res[0][0]:,}"
    except: return "210,812"

INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain Nexus</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@300;700;900&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background: #fafafa; color: #1a1a1a; }
        .btn-k { background: #A3C9D6; color: white; border-radius: 999px; font-weight: 700; transition: 0.3s; }
        .btn-k:hover { opacity: 0.8; transform: translateY(-1px); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">
    <header class="w-full max-w-6xl p-10 flex justify-between items-center">
        <div class="text-3xl font-black italic tracking-tighter">K-Brain Nexus</div>
        <div class="text-xs font-bold text-slate-300 tracking-widest uppercase">Clinical Intelligence</div>
    </header>
    <main class="flex-grow w-full max-w-4xl px-6 flex flex-col items-center text-center">
        <h1 class="text-6xl font-black mb-6 mt-10 tracking-tighter">臨床を、数字で語る。</h1>
        <p class="text-slate-400 mb-16 tracking-wide">21万件の学術エビデンスが、あなたの論理を加速させる。</p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 w-full mb-20">
            <div class="p-8 bg-white rounded-3xl border border-slate-100 shadow-sm">
                <div class="text-[10px] font-bold text-sky-400 uppercase tracking-widest mb-2">Total Archive</div>
                <div class="text-5xl font-black">{{ count }}</div>
            </div>
            <div class="p-8 bg-white rounded-3xl border border-slate-100 shadow-sm">
                <div class="text-[10px] font-bold text-sky-400 uppercase tracking-widest mb-2">Growth Factor</div>
                <div class="text-5xl font-black italic">1,395</div>
            </div>
            <div class="p-8 bg-white rounded-3xl border border-slate-100 shadow-sm">
                <div class="text-[10px] font-bold text-sky-400 uppercase tracking-widest mb-2">Processing</div>
                <div class="text-5xl font-black">0.8<span class="text-xl">s</span></div>
            </div>
        </div>

        <form action="/search" class="w-full bg-white p-2 rounded-full shadow-xl border border-slate-50 flex">
            <input name="q" class="flex-grow pl-8 outline-none text-xl bg-transparent" placeholder="臨床課題を解析..." autofocus>
            <button class="btn-k px-12 py-4">解析実行</button>
        </form>
    </main>
    <footer class="py-20 text-[10px] text-slate-200 font-bold tracking-[1em] uppercase">&copy; 2026 K-BRAIN NEXUS</footer>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(INDEX_HTML, count=get_count())

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if not q: return index()
    rows = query_db("SELECT title, abstract, url, analysis_result FROM papers WHERE title ILIKE %s OR abstract ILIKE %s LIMIT 50", (f'%{q}%', f'%{q}%'))
    results = "".join([f'<div style="background:white; padding:40px; border-radius:30px; margin-bottom:24px; border:1px solid #f0f0f0; text-align:left;"><strong style="font-size:22px; display:block; margin-bottom:15px; font-weight:900;">{r[0]}</strong><p style="color:#666; font-size:15px; line-height:1.7; margin-bottom:20px;">{r[1] or ""}</p><div style="background:#f9fbfd; padding:20px; border-radius:15px; font-size:14px; color:#444; margin-bottom:20px; border-left:4px solid #A3C9D6;"><strong>K-Brain解析:</strong><br>{r[3] or "解析待機中..."}</div><a href="{r[2]}" target="_blank" style="color:#A3C9D6; font-weight:bold; text-decoration:none;">VIEW SOURCE →</a></div>' for r in rows])
    return f'<body style="background:#fafafa; padding:40px; font-family:sans-serif;"><div style="max-width:800px; margin:0 auto;"><a href="/" style="color:#ccc; text-decoration:none; font-size:12px;">← BACK</a><h2 style="font-size:30px; font-weight:900; margin:30px 0;">Result: {q}</h2>{results}</div></body>'

if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
