import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [DB設定：RenderのStatus 1を物理的に回避] ---
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3")

# 他のAIが推奨した接続プールを、1ファイル構成に最適化して統合
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

# --- [UIデザイン：デザイナーによる「質感」と「導線」の再定義] ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078" crossorigin="anonymous"></script>
    <title>K-Brain | 臨床が変わる 破壊的な論理思考を</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@300;700;900&display=swap');
        
        body { 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            background-color: #fafafa; 
            color: #1a1a1a;
            overflow-x: hidden;
            -webkit-text-size-adjust: 100%;
        }

        /* 🌳 【絶対死守】image0(1).jpeg の質感を再現する高度なSVG背景 */
        .art-bg {
            position: fixed; top: 48%; left: 50%; transform: translate(-50%, -50%);
            width: 95%; max-width: 550px; z-index: -1; pointer-events: none;
            filter: drop-shadow(0 0 20px rgba(163, 201, 214, 0.2)); /* 水彩の滲みを表現 */
        }

        /* ロゴ：絶対に2段にならない、画面中央を維持 */
        .logo-area { white-space: nowrap; font-size: 1.875rem; font-weight: 900; font-style: italic; letter-spacing: -0.05em; }

        .hero-title { font-size: clamp(3rem, 11vw, 6.5rem); font-weight: 900; letter-spacing: -0.06em; line-height: 1.1; }
        
        /* 🔍 検索窓：スマホの枠を絶対に超えない（Padding計算） */
        .search-container { width: 100%; max-width: 600px; padding: 0 10px; box-sizing: border-box; }
        .search-pill { 
            background: white; border-radius: 999px; box-shadow: 0 10px 40px rgba(0,0,0,0.06); 
            border: 1px solid #e2e8f0; display: flex; align-items: center; padding: 6px;
        }
        .btn-search { background-color: #A3C9D6; color: white; border-radius: 999px; font-weight: 800; white-space: nowrap; padding: 12px 30px; }

        .highlight-marker { background: linear-gradient(180deg, transparent 70%, rgba(163, 201, 214, 0.3) 70%); font-weight: 700; }
        
        /* ステップカードの洗練 */
        .step-card { 
            background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px);
            border-radius: 40px; border: 1px solid #f1f5f9; box-shadow: 0 10px 30px rgba(0,0,0,0.02);
            padding: 40px; transition: transform 0.3s;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-bg">
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <filter id="soften" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="1.5" />
                </filter>
            </defs>
            <path d="M38 12C38 9 40 7 43 7H57C60 7 62 9 62 12V38H88C91 38 93 40 93 43V57C93 60 91 62 88 62H62V88C62 91 60 93 57 93H43C40 93 38 91 38 88V62H12C9 62 7 60 7 57V43C7 40 9 38 12 38H38V12Z" fill="#A3C9D6" fill-opacity="0.8" filter="url(#soften)"/>
            <path d="M48 85 C48 70 50 50 58 32" stroke="#1a1a1a" stroke-width="1.3" stroke-linecap="round"/>
            <path d="M54 62 C59 58 66 54 69 45" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M56 46 C62 42 70 38 72 28" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M46 65 C40 68 33 74 30 82" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M44 50 C38 53 30 60 28 70" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <ellipse cx="69" cy="45" rx="1.5" ry="2.2" transform="rotate(30 69 45)" fill="#1a1a1a"/>
            <ellipse cx="72" cy="28" rx="1.5" ry="2.2" transform="rotate(30 72 28)" fill="#1a1a1a"/>
            <ellipse cx="30" cy="82" rx="1.5" ry="2.2" transform="rotate(-30 30 82)" fill="#1a1a1a"/>
            <ellipse cx="28" cy="70" rx="1.5" ry="2.2" transform="rotate(-30 28 70)" fill="#1a1a1a"/>
        </svg>
    </div>

    <header class="w-full max-w-6xl px-6 py-12 flex justify-between items-center z-50">
        <div class="logo-area">K-Brain</div>
        <a href="https://ksnk-brain.jp" class="px-6 py-3 bg-black text-white text-[10px] font-bold rounded-full uppercase tracking-tighter">Launch System</a>
    </header>

    <main class="flex-grow w-full px-5 flex flex-col items-center text-center">
        <h1 class="hero-title mb-10">臨床が変わる</h1>
        <div class="space-y-4 text-lg md:text-xl text-slate-500 font-light leading-relaxed mb-16">
            <p>他職種の視点をひとつに</p>
            <p>膨大な学術データによる<br><span class="highlight-marker text-slate-900">「破壊的な論理思考」を</span></p>
        </div>

        <div class="search-container mb-24">
            <form action="/search" method="GET" class="search-pill">
                <input type="text" name="q" placeholder="臨床課題を解析..." class="flex-grow bg-transparent pl-6 pr-2 py-4 text-lg outline-none placeholder-slate-300 min-w-0">
                <button type="submit" class="btn-search text-sm">検索 🔍</button>
            </form>
        </div>

        <section class="w-full max-w-5xl grid grid-cols-1 md:grid-cols-3 gap-8 mb-32 text-left">
            <div class="step-card">
                <div class="text-4xl font-black text-slate-900 mb-6 tracking-tighter">{{ count }}</div>
                <div class="text-[10px] font-bold text-sky-600 uppercase mb-3 tracking-widest">Step 01: 疾患名・手技を入力</div>
                <p class="text-[13px] text-slate-500 leading-relaxed font-light">
                    日本語・英語どちらでも検索可能。16万件超のエビデンスから、チーム医療に必要な根拠を瞬時に特定します。
                </p>
            </div>
            <div class="step-card">
                <div class="w-12 h-12 bg-sky-50 flex items-center justify-center rounded-2xl text-sky-500 font-black mb-6">2</div>
                <div class="text-[10px] font-bold text-sky-600 uppercase mb-3 tracking-widest">Step 02: 視点の統合と解析</div>
                <p class="text-[13px] text-slate-500 leading-relaxed font-light">
                    リハと看護、異なる専門性をひとつに。現場の多職種が共通言語として使えるよう、知見を統合して解析します。
                </p>
            </div>
            <div class="step-card">
                <div class="w-12 h-12 bg-sky-50 flex items-center justify-center rounded-2xl text-sky-500 font-black mb-6">3</div>
                <div class="text-[10px] font-bold text-sky-600 uppercase mb-3 tracking-widest">Step 03: エビデンスの確認</div>
                <p class="text-[13px] text-slate-500 leading-relaxed font-light">
                    要約、引用数、関連論文を一覧で確認。PubMedへ直接リンクし、あなたの臨床的な意思決定を強力に支援します。
                </p>
            </div>
        </section>
    </main>

    <footer class="w-full py-12 text-center text-[9px] text-slate-300 font-bold tracking-[0.5em] uppercase border-t border-slate-50 bg-white">
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
    
    # 高精度なマルチワードAND検索
    terms = q.split()
    conditions = []; params = []
    for t in terms:
        conditions.append("(title ILIKE %s OR abstract ILIKE %s)")
        params.extend([f'%{t}%', f'%{t}%'])
    
    sql = f"SELECT title, abstract, url FROM papers WHERE {' AND '.join(conditions)} ORDER BY id DESC LIMIT 50"
    rows = query_db(sql, params)

    results = "".join([f'<div style="background:white; padding:40px; border-radius:40px; margin-bottom:24px; border:1px solid #f1f5f9; box-shadow:0 10px 30px rgba(0,0,0,0.02);"><strong style="display:block; font-size:22px; line-height:1.3; font-weight:900;">{r[0]}</strong><p style="font-size:16px; color:#555; line-height:1.8; margin-bottom:25px;">{r[1] or "詳細は文献を確認してください"}</p><a href="{r[2]}" target="_blank" style="display:inline-block; padding:15px 30px; background:#A3C9D6; color:white; font-size:12px; font-weight:bold; text-decoration:none; border-radius:100px;">GET EVIDENCE →</a></div>' for r in rows])
    return f'<body style="background:#fafafa; font-family:sans-serif; padding:60px 20px;"><div style="max-width:840px; margin:0 auto;"><div style="text-align:center; margin-bottom:60px;"><a href="/" style="color:#ccc; text-decoration:none; font-size:11px; font-weight:bold; letter-spacing:0.2em;">← BACK TO HOME</a><h2 style="font-size:32px; font-weight:900; margin-top:20px;">Result: {q}</h2></div>{results}</div></body>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
