import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [DB設定：高速・安定な接続プール] ---
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3")

pool = SimpleConnectionPool(minconn=1, maxconn=5, dsn=DATABASE_URL)

def query_db(sql, params=None):
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

# --- [UI：シンボルの死守と意思決定支援の器] ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>K-Brain | 臨床が変わる 破壊的な論理思考を</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@300;700;900&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #fafafa; color: #1a1a1a; overflow-x: hidden; }

        /* 🌳 聖域：image0 (1).jpeg を完全再現（消えない・崩れない） */
        .art-bg {
            position: fixed; top: 48%; left: 50%; transform: translate(-50%, -50%);
            width: 95%; max-width: 550px; z-index: -1; pointer-events: none;
        }

        .hero-title { font-size: clamp(3rem, 11vw, 6.5rem); font-weight: 900; letter-spacing: -0.06em; line-height: 1.1; margin-bottom: 2rem; }
        .hero-sub { font-size: clamp(1.1rem, 2.5vw, 1.4rem); font-weight: 400; color: #475467; line-height: 1.6; }
        .search-pill { background: white; border-radius: 999px; box-shadow: 0 10px 40px rgba(0,0,0,0.04); border: 1px solid #e2e8f0; width: 100%; box-sizing: border-box; }
        .btn-search { background-color: #A3C9D6; color: white; border-radius: 999px; font-weight: 800; white-space: nowrap; }
        .highlight { background: linear-gradient(180deg, transparent 75%, rgba(163, 201, 214, 0.4) 75%); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-bg">
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M38 12C38 9 40 7 43 7H57C60 7 62 9 62 12V38H88C91 38 93 40 93 43V57C93 60 91 62 88 62H62V88C62 91 60 93 57 93H43C40 93 38 91 38 88V62H12C9 62 7 60 7 57V43C7 40 9 38 12 38H38V12Z" fill="#A3C9D6" fill-opacity="0.8"/>
            <path d="M48 85 C48 70 50 50 58 32" stroke="#1a1a1a" stroke-width="1.3" stroke-linecap="round"/>
            <path d="M54 62 C59 58 66 54 69 45" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M56 46 C62 42 70 38 72 28" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M46 65 C40 68 33 74 30 82" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M44 50 C38 53 30 60 28 70" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <circle cx="69" cy="45" r="1.2" fill="#1a1a1a"/><circle cx="72" cy="28" r="1.2" fill="#1a1a1a"/>
            <circle cx="30" cy="82" r="1.2" fill="#1a1a1a"/><circle cx="28" cy="70" r="1.2" fill="#1a1a1a"/>
        </svg>
    </div>

    <header class="w-full max-w-6xl px-6 py-10 flex justify-between items-center z-50">
        <div class="text-3xl font-black italic tracking-tighter whitespace-nowrap">K-Brain</div>
        <a href="https://ksnk-brain.jp" class="px-6 py-3 bg-black text-white text-[10px] font-bold rounded-full tracking-tighter whitespace-nowrap uppercase">Launch System</a>
    </header>

    <main class="flex-grow flex flex-col items-center w-full px-5 text-center">
        <h1 class="hero-title">臨床が変わる</h1>
        <div class="hero-sub mb-16 space-y-4">
            <p>他職種の視点をひとつに</p>
            <p>膨大な学術データによる<br><span class="highlight font-bold text-slate-900">「破壊的な論理思考」を</span></p>
        </div>

        <div class="w-full max-w-2xl px-2 mb-24">
            <div class="search-pill p-1.5 flex items-center">
                <form action="/search" method="GET" class="flex w-full items-center">
                    <input type="text" name="q" placeholder="臨床課題を解析..." class="flex-grow bg-transparent pl-5 pr-2 py-4 text-lg outline-none placeholder-slate-300 min-w-0">
                    <button type="submit" class="btn-search px-8 py-4 text-sm">検索 🔍</button>
                </form>
            </div>
        </div>

        <section class="w-full max-w-5xl grid grid-cols-1 md:grid-cols-3 gap-6 mb-32 text-left">
            <div class="bg-white p-10 rounded-[40px] border border-slate-50 shadow-sm space-y-4">
                <div class="text-4xl font-black">{{ count }}</div>
                <div class="text-[10px] font-bold text-sky-600 uppercase tracking-widest">Step 01: 疾患名・手技を入力</div>
                <p class="text-[13px] text-slate-500 leading-relaxed">日本語・英語を問わず、16万件超の知能アーカイブから臨床の問いに合致するエビデンスを特定します。</p>
            </div>
            <div class="bg-white p-10 rounded-[40px] border border-slate-50 shadow-sm space-y-4">
                <div class="w-12 h-12 bg-sky-50 flex items-center justify-center rounded-2xl text-sky-500 font-black">2</div>
                <div class="text-[10px] font-bold text-sky-600 uppercase tracking-widest">Step 02: 視点の統合と解析</div>
                <p class="text-[13px] text-slate-500 leading-relaxed">リハと看護、異なる専門職の知見を統合。現場で即座に共有できる「共通言語」へと解析します。</p>
            </div>
            <div class="bg-white p-10 rounded-[40px] border border-slate-50 shadow-sm space-y-4">
                <div class="w-12 h-12 bg-sky-50 flex items-center justify-center rounded-2xl text-sky-500 font-black">3</div>
                <div class="text-[10px] font-bold text-sky-600 uppercase tracking-widest">Step 03: エビデンスの確認</div>
                <p class="text-[13px] text-slate-500 leading-relaxed">要約・引用・関連論文を一覧化。確固たる根拠が、あなたの「破壊的な論理思考」を確信へと変えます。</p>
            </div>
        </section>
    </main>

    <footer class="w-full py-12 text-center text-[9px] text-slate-300 font-bold tracking-[0.5em] uppercase border-t border-slate-50">
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
        conn = pool.getconn(); cur = conn.cursor()
        # 簡易AND検索ロジック
        terms = q.split()
        conditions = []; params = []
        for t in terms:
            conditions.append("(title ILIKE %s OR abstract ILIKE %s)")
            params.extend([f'%{t}%', f'%{t}%'])
        
        sql = f"SELECT title, abstract, url FROM papers WHERE {' AND '.join(conditions)} ORDER BY id DESC LIMIT 50"
        cur.execute(sql, params)
        rows = cur.fetchall(); cur.close()

        results = "".join([f'<div style="background:white; padding:40px; border-radius:40px; margin-bottom:24px; border:1px solid #f1f5f9; box-shadow:0 10px 30px rgba(0,0,0,0.02);"><strong style="display:block; font-size:20px; line-height:1.4; margin-bottom:15px; font-weight:900;">{r[0]}</strong><p style="font-size:15px; color:#555; line-height:1.8; margin-bottom:25px;">{r[1] or "詳細は文献を確認してください"}</p><a href="{r[2]}" target="_blank" style="display:inline-block; padding:15px 30px; background:#A3C9D6; color:white; font-size:12px; font-weight:bold; text-decoration:none; border-radius:100px;">GET EVIDENCE →</a></div>' for r in rows])
        
        # 意思決定支援AIの「返答」を想定したヘッダー
        header = f'<div style="text-align:center; margin-bottom:60px;"><a href="/" style="color:#ccc; text-decoration:none; font-size:11px; font-weight:bold; letter-spacing:0.2em;">← BACK TO HOME</a><h2 style="font-size:32px; font-weight:900; margin-top:20px;">Analysis for "{q}"</h2></div>'
        
        return f'<body style="background:#fafafa; font-family:sans-serif; padding:60px 20px;"><div style="max-width:840px; margin:0 auto;">{header}{results}</div></body>'
    except Exception as e: return str(e)
    finally:
        if conn: pool.putconn(conn)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
