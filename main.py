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
    <title>K-Brain | Numeric Manifesto</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@100;400;700;900&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #fafafa; }
        .art-bg { position: fixed; top: 48%; left: 50%; transform: translate(-50%, -50%); width: 95%; max-width: 530px; z-index: -1; opacity: 0.95; pointer-events: none; }
        .metric-card { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); padding: 3rem; border-radius: 48px; border: 1px solid rgba(0,0,0,0.02); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">
    <div class="art-bg">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <path d="M40 8 Q38 8 38 12 L38 38 L12 38 Q8 38 8 42 L8 58 Q8 62 12 62 L38 62 L38 88 Q38 92 42 92 L58 92 Q62 92 62 88 L62 62 L88 62 Q92 62 92 58 L92 42 Q92 38 88 38 L62 38 L62 12 Q62 8 58 8 Z" fill="#A3C9D6" fill-opacity="0.9" />
            <path d="M50 88 C49 70 51 52 58 35" stroke="#1a1a1a" stroke-width="1.3" fill="none" stroke-linecap="round" />
            <path d="M54 65 C60 62 67 58 70 48" stroke="#1a1a1a" stroke-width="1.0" fill="none" stroke-linecap="round" />
            <path d="M46 68 C40 70 34 78 32 86" stroke="#1a1a1a" stroke-width="1.0" fill="none" stroke-linecap="round" />
            <path d="M70 48 Q72 46 71.5 49.5 Q71 53 69 48.5 Z" fill="#1a1a1a"/><path d="M32 86 Q30 88 30.5 84.5 Q31 81 33 85.5 Z" fill="#1a1a1a"/>
        </svg>
    </div>
    <header class="w-full max-w-6xl px-8 py-10 flex justify-between items-center z-50"><div class="text-3xl font-black italic">K-Brain</div></header>
    <main class="flex-grow w-full px-6 flex flex-col items-center text-center">
        <h1 class="text-6xl md:text-8xl font-black mb-16 tracking-tighter">臨床を、数字で語る。</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 w-full mb-24 text-left">
            <div class="metric-card"><div class="text-6xl font-black mb-4 tracking-tighter">{{ count }}</div><div class="text-[10px] font-bold text-sky-600 uppercase tracking-widest">Total Archive Index</div></div>
            <div class="metric-card border-t-8 border-t-[#A3C9D6]"><div class="text-6xl font-black mb-4 italic tracking-tighter">1,398</div><div class="text-[10px] font-bold text-sky-600 uppercase tracking-widest">Growth Factor</div></div>
            <div class="metric-card"><div class="text-6xl font-black mb-4 tracking-tighter">0.8<span class="text-2xl">s</span></div><div class="text-[10px] font-bold text-sky-600 uppercase tracking-widest">Logic Latency</div></div>
        </div>
        <form action="/search" class="w-full max-w-2xl bg-white rounded-full shadow-2xl flex p-2 border border-slate-100">
            <input name="q" class="flex-grow pl-8 outline-none text-xl bg-transparent" placeholder="臨床課題を解析...">
            <button class="bg-[#A3C9D6] text-white px-12 py-4 rounded-full font-bold">解析 🔍</button>
        </form>
    </main>
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
    results = "".join([f'<div style="background:white; padding:40px; border-radius:35px; margin-bottom:24px; border:1px solid #f1f5f9; box-shadow:0 10px 30px rgba(0,0,0,0.02); text-align:left;"><strong style="display:block; font-size:22px; line-height:1.4; font-weight:900;">{r[0]}</strong><p style="font-size:16px; color:#555; line-height:1.8; margin:20px 0;">{r[1] or "詳細は文献を確認してください"}</p><a href="{r[2]}" target="_blank" style="display:inline-block; padding:15px 30px; background:#A3C9D6; color:white; font-size:12px; font-weight:bold; text-decoration:none; border-radius:100px;">VIEW EVIDENCE →</a></div>' for r in rows])
    return f'<body style="background:#fafafa; font-family:sans-serif; padding:60px 20px;"><div style="max-width:840px; margin:0 auto;"><a href="/" style="color:#ccc; text-decoration:none; font-size:12px; font-weight:bold;">← BACK</a><h2 style="font-size:32px; font-weight:900; margin:30px 0;">Result: {q}</h2>{results}</div></body>'

if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
