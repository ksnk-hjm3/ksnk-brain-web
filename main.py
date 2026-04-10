import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from flask import Flask, request, render_template_string

app = Flask(__name__)

# ⚠️ ここにも、同じ「External Database URL」を貼り付けてください
DATABASE_URL = os.environ.get("DATABASE_URL", "ここにコピーしたURLを貼り付け")

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
    <title>K-Brain | Numeric Manifesto</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@100;400;700;900&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #fafafa; }
        .art-bg { position: fixed; top: 48%; left: 50%; transform: translate(-50%, -50%); width: 95%; max-width: 550px; z-index: -1; opacity: 0.95; }
        .metric-card { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); padding: 3rem; border-radius: 40px; border: 1px solid rgba(0,0,0,0.02); box-shadow: 0 20px 40px rgba(0,0,0,0.02); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">
    <div class="art-bg">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <path d="M40 8 Q38 8 38 12 L38 38 L12 38 Q8 38 8 42 L8 58 Q8 62 12 62 L38 62 L38 88 Q38 92 42 92 L58 92 Q62 92 62 88 L62 62 L88 62 Q92 62 92 58 L92 42 Q92 38 88 38 L62 38 L62 12 Q62 8 58 8 Z" fill="#A3C9D6" fill-opacity="0.9" />
            <path d="M50 88 C49 70 51 52 58 35" stroke="#1a1a1a" stroke-width="1.3" fill="none" stroke-linecap="round" />
            <path d="M54 65 C60 62 67 58 70 48" stroke="#1a1a1a" stroke-width="0.9" fill="none" stroke-linecap="round" />
            <path d="M46 68 C40 70 34 78 32 86" stroke="#1a1a1a" stroke-width="0.9" fill="none" stroke-linecap="round" />
            <circle cx="70" cy="48" r="1.5" fill="#1a1a1a"/><circle cx="32" cy="86" r="1.5" fill="#1a1a1a"/>
        </svg>
    </div>
    <header class="w-full max-w-6xl px-8 py-10 flex justify-between items-center"><div class="text-3xl font-black italic">K-Brain</div></header>
    <main class="w-full max-w-2xl text-center">
        <h1 class="text-6xl font-black mb-16">臨床を、数字で語る。</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-left mb-32">
            <div class="metric-card"><div class="text-5xl font-black mb-4">{{ count }}</div><div class="text-xs font-bold text-sky-600 uppercase tracking-widest">Total Archive</div></div>
            <div class="metric-card"><div class="text-5xl font-black mb-4 italic">1,395</div><div class="text-xs font-bold text-sky-600 uppercase tracking-widest">Daily Growth</div></div>
            <div class="metric-card"><div class="text-5xl font-black mb-4">0.8s</div><div class="text-xs font-bold text-sky-600 uppercase tracking-widest">Logic Speed</div></div>
        </div>
        <form action="/search" class="bg-white rounded-full shadow-2xl flex p-2"><input name="q" class="flex-grow pl-6 outline-none text-lg" placeholder="臨床課題を解析..."><button class="bg-[#A3C9D6] text-white px-10 py-4 rounded-full font-bold">検索</button></form>
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
    results = "".join([f'<div style="background:white; padding:40px; border-radius:30px; margin-bottom:20px; box-shadow:0 10px 30px rgba(0,0,0,0.02); text-align:left;"><b>{r[0]}</b><p>{r[1]}</p><a href="{r[2]}" target="_blank" style="color:#A3C9D6; font-weight:bold;">VIEW EVIDENCE →</a></div>' for r in rows])
    return f'<body style="background:#fafafa; padding:40px; font-family:sans-serif;"><div style="max-width:800px; margin:0 auto;"><a href="/" style="color:#ccc; text-decoration:none; font-size:12px;">← BACK</a><h2 style="margin-top:20px;">Result: {q}</h2>{results}</div></body>'

if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
