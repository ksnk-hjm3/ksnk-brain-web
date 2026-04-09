import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [設定エリア] ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def get_evidence_count():
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM papers")
        count = cur.fetchone()[0]
        cur.close(); conn.close()
        return "{:,}".format(count)
    except: return "168,349"

# --- [HTMLデザイン] ---
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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Noto+Sans+JP:wght@300;500;700;900&display=swap');
        
        body { 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            background-color: #fafafa; 
            color: #1a1a1a;
            overflow-x: hidden;
            -webkit-text-size-adjust: 100%;
        }

        /* 🌳 アップロード画像(image0 (1).jpeg)を忠実に再現した背景 */
        .art-bg {
            position: fixed;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 90%;
            max-width: 500px;
            z-index: -1;
            opacity: 0.15;
            pointer-events: none;
        }

        .hero-title {
            font-size: clamp(2.8rem, 8vw, 5.5rem);
            font-weight: 900;
            letter-spacing: -0.05em;
            line-height: 1.1;
        }

        /* 🔍 検索バーのスマホ最適化 */
        .search-pill {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border: 1px solid #e2e8f0;
            border-radius: 999px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
            width: 100%;
            max-width: 600px;
        }

        .status-card {
            background: white;
            border-radius: 20px;
            border: 1px solid #f1f5f9;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        }

        .highlight-blue {
            background: linear-gradient(180deg, transparent 70%, rgba(163, 201, 214, 0.3) 70%);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-bg">
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M38 10C38 8 40 6 42 6H58C60 6 62 8 62 10V38H90C92 38 94 40 94 42V58C94 60 92 62 90 62H62V90C62 92 60 94 58 94H42C40 94 38 92 38 90V62H10C8 62 6 60 6 58V42C6 40 8 38 10 38H38V10Z" fill="#A3C9D6" fill-opacity="0.8"/>
            <path d="M52 88C52 75 54 55 60 35" stroke="#1a1a1a" stroke-width="1.2" stroke-linecap="round"/>
            <path d="M55 65C60 60 68 55 72 42" stroke="#1a1a1a" stroke-width="0.8" stroke-linecap="round"/>
            <path d="M57 45C64 40 72 35 75 25" stroke="#1a1a1a" stroke-width="0.8" stroke-linecap="round"/>
            <path d="M48 68C42 70 34 76 30 85" stroke="#1a1a1a" stroke-width="0.8" stroke-linecap="round"/>
            <path d="M47 50C40 53 30 62 28 72" stroke="#1a1a1a" stroke-width="0.8" stroke-linecap="round"/>
            <circle cx="72" cy="42" r="1.2" fill="#1a1a1a"/><circle cx="75" cy="25" r="1.2" fill="#1a1a1a"/>
            <circle cx="30" cy="85" r="1.2" fill="#1a1a1a"/><circle cx="28" cy="72" r="1.2" fill="#1a1a1a"/>
        </svg>
    </div>

    <header class="w-full max-w-7xl px-6 py-8 flex justify-between items-center z-50">
        <div class="text-3xl font-black italic tracking-tighter whitespace-nowrap">K-Brain</div>
        <div class="flex items-center space-x-6">
            <a href="https://www.instagram.com/ksnk.hjm3/" class="text-[10px] font-bold text-slate-400 uppercase tracking-widest hidden sm:block">Instagram</a>
            <a href="https://ksnk-brain.jp" class="px-5 py-2.5 bg-black text-white text-[10px] font-bold rounded-full uppercase tracking-tighter whitespace-nowrap">Launch System</a>
        </div>
    </header>

    <main class="flex-grow flex flex-col items-center w-full px-5 text-center">
        <div class="mt-12 mb-20 space-y-8">
            <h1 class="hero-title">臨床が変わる</h1>
            <div class="space-y-3">
                <p class="text-lg md:text-xl font-light text-slate-500">他職種の視点をひとつに</p>
                <p class="text-lg md:text-xl font-light text-slate-500">膨大な学術データによる<span class="highlight-blue font-bold text-slate-900">「破壊的な論理思考」</span>を</p>
            </div>
        </div>

        <div class="search-pill p-1.5 flex items-center mb-24">
            <form action="/search" method="GET" class="flex w-full items-center">
                <input type="text" name="q" placeholder="臨床課題を入力..." class="flex-grow bg-transparent pl-5 pr-2 py-4 text-base outline-none placeholder-slate-300 min-w-0">
                <button type="submit" class="bg-[#A3C9D6] text-white px-6 py-4 rounded-full font-bold text-sm whitespace-nowrap shadow-sm">
                    検索 🔍
                </button>
            </form>
        </div>

        <section class="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-4 mb-24 text-left">
            <div class="status-card p-6 flex items-center space-x-4">
                <div class="text-3xl font-black text-slate-900">{{ count }}</div>
                <div class="text-[9px] text-slate-400 font-bold uppercase tracking-widest">収録エビデンス数</div>
            </div>
            <div class="status-card p-6 flex items-center space-x-4">
                <div class="text-3xl font-black text-slate-900">12分野</div>
                <div class="text-[9px] text-slate-400 font-bold uppercase tracking-widest">対応領域</div>
            </div>
            <div class="status-card p-6 flex items-center space-x-4">
                <div class="text-3xl font-black text-slate-900">Weekly</div>
                <div class="text-[9px] text-slate-400 font-bold uppercase tracking-widest">知能更新</div>
            </div>
        </section>

        <section class="w-full max-w-4xl mb-32 space-y-12">
            <h2 class="text-xs font-bold text-slate-300 tracking-[0.5em] uppercase">How To Use</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="p-8 bg-white rounded-[32px] border border-slate-50 text-left space-y-4">
                    <div class="text-sky-500 font-bold text-xs uppercase">Step 01</div>
                    <div class="text-xl font-bold">疾患名・手技を入力</div>
                    <p class="text-sm text-slate-400 leading-relaxed">日本語・英語どちらでも検索可能 AND/OR検索にも対応</p>
                </div>
                <div class="p-8 bg-white rounded-[32px] border border-slate-50 text-left space-y-4">
                    <div class="text-sky-500 font-bold text-xs uppercase">Step 02</div>
                    <div class="text-xl font-bold">フィルターで絞り込み</div>
                    <p class="text-sm text-slate-400 leading-relaxed">発行年・ジャーナル・言語で素早く目的の論文へ</p>
                </div>
                <div class="p-8 bg-white rounded-[32px] border border-slate-50 text-left space-y-4">
                    <div class="text-sky-500 font-bold text-xs uppercase">Step 03</div>
                    <div class="text-xl font-bold">エビデンスを確認</div>
                    <p class="text-sm text-slate-400 leading-relaxed">要約・引用数・関連論文を一覧で確認 PubMedへ直接リンク</p>
                </div>
            </div>
        </section>
    </main>

    <footer class="w-full py-12 border-t border-slate-100 text-center bg-white">
        <div class="text-[9px] text-slate-300 font-bold tracking-[0.5em] uppercase">&copy; 2026 K-BRAIN NEXUS PROJECT</div>
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, count=get_evidence_count())

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query: return render_template_string(INDEX_HTML, count=get_evidence_count())
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT title, abstract, url FROM papers WHERE title ILIKE %s OR abstract ILIKE %s ORDER BY id DESC LIMIT 50", (f'%{query}%', f'%{query}%'))
        rows = cur.fetchall(); cur.close(); conn.close()
        results = "".join([f'<div style="background:white; padding:35px; border-radius:30px; margin-bottom:20px; border:1px solid #f1f5f9; box-shadow:0 10px 30px -10px rgba(0,0,0,0.03);"><strong style="display:block; font-size:20px; margin-bottom:15px; line-height:1.3;">{r[0]}</strong><p style="font-size:15px; color:#666; line-height:1.7; margin-bottom:20px;">{r[1] or "詳細は文献を確認してください"}</p><a href="{r[2]}" target="_blank" style="color:#A3C9D6; font-weight:bold; text-decoration:none; font-size:13px; letter-spacing:0.1em;">GET EVIDENCE →</a></div>' for r in rows])
        return f'<body style="background:#fafafa; font-family:sans-serif; padding:40px 20px;"><div style="max-width:800px; margin:0 auto;"><div style="text-align:center; margin-bottom:50px;"><a href="/" style="color:#ccc; text-decoration:none; font-size:12px; font-weight:bold; letter-spacing:0.2em;">← BACK TO HOME</a><h2 style="font-size:32px; font-weight:900; margin-top:20px;">Results: {query}</h2></div>{results}</div></body>'
    except Exception as e: return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
