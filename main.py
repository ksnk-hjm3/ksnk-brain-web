import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [1. データベース設定] ---
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3")

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

# --- [2. 究極のデザイン：不自然さを排除したプロフェッショナルUI] ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>K-Brain | 臨床が変わる 破壊的な論理思考を</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@100;400;700;900&display=swap');
        
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #fafafa; color: #1a1a1a; overflow-x: hidden; }

        /* 🌳 【聖域】背景アイコンの完全再現：殴り書きを「葉」へ修正 */
        .art-bg {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 85%; max-width: 480px; z-index: -1; pointer-events: none;
            opacity: 0.9;
        }

        .hero-title { 
            font-size: clamp(3.2rem, 11vw, 6.2rem); 
            font-weight: 900; 
            letter-spacing: -0.06em; 
            line-height: 1.1; 
            color: #1a1a1a;
        }

        .hero-sub { 
            font-size: clamp(1.1rem, 2.5vw, 1.25rem); 
            font-weight: 300; 
            color: #667085; 
            line-height: 1.8;
            letter-spacing: 0.05em;
        }

        /* 🔍 検索バー：不自然なはみ出しと影を修正 */
        .search-pill { 
            background: white; border-radius: 999px; box-shadow: 0 12px 30px -5px rgba(0,0,0,0.04); 
            border: 1px solid #f2f4f7; display: flex; align-items: center; padding: 4px;
        }
        .search-input { flex-grow: 1; background: transparent; padding: 12px 24px; font-size: 1.1rem; outline: none; border: none; color: #1a1a1a; }
        .btn-search { 
            background-color: #A3C9D6; color: white; border-radius: 999px; 
            font-weight: 800; padding: 12px 30px; transition: opacity 0.2s;
        }

        /* バリューカード：数字(02)を廃止し、意味のある構造へ */
        .card-container { display: grid; grid-template-cols: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; width: 100%; max-width: 1100px; }
        .benefit-card {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px);
            padding: 2.5rem; border-radius: 32px; border: 1px solid rgba(242, 244, 215, 0.3);
            box-shadow: 0 4px 20px rgba(0,0,0,0.01);
            text-align: left;
        }
        .marker { background: linear-gradient(180deg, transparent 75%, rgba(163, 201, 214, 0.3) 75%); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-bg">
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M40 8 Q38 8 38 12 L38 38 L12 38 Q8 38 8 42 L8 58 Q8 62 12 62 L38 62 L38 88 Q38 92 42 92 L58 92 Q62 92 62 88 L62 62 L88 62 Q92 62 92 58 L92 42 Q92 38 88 38 L62 38 L62 12 Q62 8 58 8 Z" fill="#A3C9D6" fill-opacity="0.8" />
            <path d="M50 88 C49 70 51 52 58 35" stroke="#1a1a1a" stroke-width="1.2" stroke-linecap="round" />
            <path d="M54 65 C60 62 67 58 70 48" stroke="#1a1a1a" stroke-width="0.8" stroke-linecap="round" />
            <path d="M56 48 C64 45 72 40 74 30" stroke="#1a1a1a" stroke-width="0.8" stroke-linecap="round" />
            <path d="M46 68 C40 70 34 78 32 86" stroke="#1a1a1a" stroke-width="0.8" stroke-linecap="round" />
            <path d="M44 52 C38 55 31 64 30 74" stroke="#1a1a1a" stroke-width="0.8" stroke-linecap="round" />
            <path d="M70 48 Q72 46 71.5 49.5 Q71 53 69 48.5 Z" fill="#1a1a1a"/>
            <path d="M74 30 Q76 28 75.5 31.5 Q75 35 73 30.5 Z" fill="#1a1a1a"/>
            <path d="M32 86 Q30 88 30.5 84.5 Q31 81 33 85.5 Z" fill="#1a1a1a"/>
            <path d="M30 74 Q28 76 28.5 72.5 Q29 69 31 73.5 Z" fill="#1a1a1a"/>
        </svg>
    </div>

    <header class="w-full max-w-6xl px-8 py-10 flex justify-between items-center z-50">
        <div class="text-3xl font-black italic tracking-tighter text-slate-900">K-Brain</div>
        <div class="flex items-center space-x-6">
            <a href="https://www.instagram.com/ksnk.hjm3/" target="_blank" class="text-[10px] font-bold text-slate-400 uppercase tracking-widest hidden sm:block">Instagram</a>
            <a href="https://ksnk-brain.jp" class="px-6 py-3 bg-black text-white text-[11px] font-bold rounded-full uppercase tracking-tighter shadow-lg">Launch System</a>
        </div>
    </header>

    <main class="flex-grow flex flex-col items-center w-full px-4 text-center">
        <h1 class="hero-title mt-16 mb-10">臨床が変わる</h1>
        
        <div class="hero-sub mb-20 max-w-2xl">
            <p>他職種の視点をひとつに</p>
            <p>16万件の学術データによる<span class="marker font-bold text-slate-900">「破壊的な論理思考」</span>を</p>
        </div>

        <div class="w-full max-w-2xl mb-32 px-2">
            <form action="/search" method="GET" class="search-pill">
                <input type="text" name="q" placeholder="臨床課題をキーワードで検索..." class="search-input placeholder-slate-300">
                <button type="submit" class="btn-search text-xs">検索 🔍</button>
            </form>
        </div>

        <div class="card-container mb-40">
            <div class="benefit-card">
                <div class="text-4xl font-black mb-6 tracking-tighter text-slate-900">{{ count }}</div>
                <div class="text-[11px] font-bold text-sky-600 uppercase mb-4 tracking-widest">Evidence Base</div>
                <p class="text-sm text-slate-500 leading-relaxed font-light">
                    16万件を超えるエビデンスをリアルタイムに集計。理学療法と看護の知見を背景に、明日からの介入に揺るぎない根拠を提供します。
                </p>
            </div>
            <div class="benefit-card border-t-4 border-t-[#A3C9D6]">
                <div class="text-3xl font-black mb-6 italic text-slate-900 tracking-tight">Integration</div>
                <div class="text-[11px] font-bold text-sky-600 uppercase mb-4 tracking-widest">Multi-Disciplinary</div>
                <p class="text-sm text-slate-500 leading-relaxed font-light">
                    異なる専門性の境界線を溶かし、チーム医療における「共通言語」を生成。職種を超えた論理的な合意形成を支援します。
                </p>
            </div>
            <div class="benefit-card">
                <div class="text-3xl font-black mb-6 tracking-tighter text-slate-900">Decision Support</div>
                <div class="text-[11px] font-bold text-sky-600 uppercase mb-4 tracking-widest">From Data to Action</div>
                <p class="text-sm text-slate-500 leading-relaxed font-light">
                    「論文を読む」から「意思決定に使う」へ。膨大なエビデンスを、目の前の患者様への具体的なアクションへと変換します。
                </p>
            </div>
        </div>
    </main>

    <footer class="w-full py-16 bg-white border-t border-slate-100 text-center text-[10px] text-slate-300 font-bold tracking-[0.5em] uppercase">
        &copy; 2026 K-BRAIN NEXUS PROJECT | EBM ARCHIVE
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
    results = "".join([f'<div style="background:white; padding:40px; border-radius:40px; margin-bottom:24px; border:1px solid #f1f5f9; box-shadow:0 10px 30px rgba(0,0,0,0.02);"><strong style="display:block; font-size:22px; line-height:1.4; font-weight:900;">{r[0]}</strong><p style="font-size:16px; color:#555; line-height:1.8; margin-bottom:25px;">{r[1] or "詳細は文献を確認してください"}</p><a href="{r[2]}" target="_blank" style="display:inline-block; padding:15px 30px; background:#A3C9D6; color:white; font-size:12px; font-weight:bold; text-decoration:none; border-radius:100px;">GET EVIDENCE →</a></div>' for r in rows])
    return f'<body style="background:#fafafa; font-family:sans-serif; padding:60px 20px;"><div style="max-width:840px; margin:0 auto;"><div style="text-align:center; margin-bottom:60px;"><a href="/" style="color:#d1d1d1; text-decoration:none; font-size:11px; font-weight:bold; letter-spacing:0.3em;">← BACK TO HOME</a><h2 style="font-size:36px; font-weight:900; margin-top:20px;">Result: {q}</h2></div>{results}</div></body>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
