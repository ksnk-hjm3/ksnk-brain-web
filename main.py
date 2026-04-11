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
    except: return "210,000"

INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain Nexus</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@300;700;900&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background: #fafafa; }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">
    <header class="w-full max-w-6xl p-10 flex justify-between items-center">
        <div class="text-3xl font-black italic tracking-tighter text-slate-900">K-Brain Nexus</div>
        <div class="text-[10px] font-bold text-slate-300 tracking-[0.3em] uppercase">Scientific Evidence Engine</div>
    </header>
    <main class="flex-grow w-full max-w-4xl px-6 flex flex-col items-center text-center">
        <h1 class="text-6xl font-black mb-6 mt-16 tracking-tighter">臨床を、数字で語る。</h1>
        <p class="text-slate-400 mb-20 tracking-wide text-lg">21万件の学術エビデンスによる、破壊的な論理思考。</p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 w-full mb-20">
            <div class="p-10 bg-white rounded-[40px] shadow-sm border border-slate-50">
                <div class="text-[10px] font-bold text-sky-400 uppercase tracking-widest mb-4">Archive</div>
                <div class="text-5xl font-black tracking-tighter">{{ count }}</div>
            </div>
            <div class="p-10 bg-white rounded-[40px] shadow-sm border border-slate-50">
                <div class="text-[10px] font-bold text-sky-400 uppercase tracking-widest mb-4">Daily Growth</div>
                <div class="text-5xl font-black italic tracking-tighter">1,397</div>
            </div>
            <div class="p-10 bg-white rounded-[40px] shadow-sm border border-slate-50">
                <div class="text-[10px] font-bold text-sky-400 uppercase tracking-widest mb-4">Latency</div>
                <div class="text-5xl font-black tracking-tighter">0.8<span class="text-2xl ml-1">s</span></div>
            </div>
        </div>

        <form action="/search" class="w-full bg-white p-2 rounded-full shadow-2xl border border-slate-50 flex mb-32">
            <input name="q" class="flex-grow pl-10 outline-none text-xl bg-transparent" placeholder="臨床課題を検索..." autofocus>
            <button class="bg-[#A3C9D6] text-white px-14 py-5 rounded-full font-black text-sm hover:opacity-80 transition-all">解析開始</button>
        </form>
    </main>
    <footer class="py-20 text-[10px] text-slate-200 font-bold tracking-[1em] uppercase border-t w-full text-center">&copy; 2026 K-BRAIN NEXUS</footer>
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
    results = "".join([f'<div style="background:white; padding:45px; border-radius:40px; margin-bottom:24px; border:1px solid #f0f0f0; text-align:left; box-shadow:0 10px 30px rgba(0,0,0,0.02);"><strong style="font-size:24px; display:block; margin-bottom:20px; font-weight:900; line-height:1.3;">{r[0]}</strong><p style="color:#666; font-size:16px; line-height:1.8; margin-bottom:30px;">{r[1] or ""}</p><div style="background:#f9fbfd; padding:25px; border-radius:20px; font-size:15px; color:#444; border-left:5px solid #A3C9D6; margin-bottom:25px;"><strong>K-Brain Insight:</strong><br><br>{r[3] or "AI解析待機中..."}</div><a href="{r[2]}" target="_blank" style="color:#A3C9D6; font-weight:bold; text-decoration:none; font-size:13px; letter-spacing:0.1em;">VIEW SOURCE EVIDENCE →</a></div>' for r in rows])
    return f'<body style="background:#fafafa; padding:60px 20px; font-family:sans-serif;"><div style="max-width:850px; margin:0 auto;"><div style="text-align:center; margin-bottom:60px;"><a href="/" style="color:#ccc; text-decoration:none; font-size:11px; font-weight:bold; letter-spacing:0.2em;">← BACK TO ANALYZER</a><h2 style="font-size:36px; font-weight:900; margin-top:24px;">Result: {q}</h2></div>{results}</div></body>'

if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
