import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [設定エリア] ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# --- [デザイン：Minimal Medical Grace] ---
# 提供された画像のミニマルで清潔なテイスト（白背景、水色十字、黒植物）を全面的に採用
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078" crossorigin="anonymous"></script>
    <title>K-Brain | 統合知能アーカイブ</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Noto+Sans+JP:wght@300;500;700&display=swap');
        
        body { 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            background-color: #ffffff; 
            color: #101828;
            overflow-x: hidden;
        }

        .hero-title {
            letter-spacing: -0.04em;
            line-height: 1.05;
            background: linear-gradient(180deg, #101828 0%, #475467 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* 💡 検索窓：丸みとアクセントカラー（水色） */
        .search-card {
            background: #ffffff;
            border: 1px solid #e4e7ec;
            border-radius: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 10px 15px -3px rgba(0, 0, 0, 0.03);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .search-card:focus-within {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(163, 207, 234, 0.8); /* 医療十字の水色 */
        }

        .btn-premium {
            background: #a3cfea; /* 医療十字の水色 */
            color: #101828;
            transition: all 0.2s ease;
        }

        .btn-premium:hover {
            background: #ffffff;
            color: #a3cfea;
            border: 1px solid #a3cfea;
            box-shadow: 0 4px 10px rgba(163, 207, 234, 0.4);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <div class="fixed inset-0 flex items-center justify-center z-[-1]">
        <svg class="w-[80vw] h-[80vh] opacity-10" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M35 15C35 12.2386 37.2386 10 40 10H60C62.7614 10 65 12.2386 65 15V35H85C87.7614 35 90 37.2386 90 40V60C90 62.7614 87.7614 65 85 65H65V85C65 87.7614 62.7614 90 60 90H40C37.2386 90 35 87.7614 35 85V65H15C12.2386 65 10 62.7614 10 60V40C10 37.2386 12.2386 35 15 35H35V15Z" fill="#a3cfea" fill-opacity="0.8"/>
            <path d="M50 85C50 70 51.5 55 53 40" stroke="black" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M51 60C53 58 55 56 57 54C58.3 52.7 59 51 59 49" stroke="black" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M52 50C54 48 56 46 58 44C59.3 42.7 60 41 60 39" stroke="black" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M53 40C55 38 57 36 59 34C60.3 32.7 61 31 61 29" stroke="black" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M49 60C47 62 45 64 43 66C41.7 67.3 41 69 41 71" stroke="black" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M48 50C46 52 44 54 42 56C40.7 57.3 40 59 40 61" stroke="black" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M47 40C45 42 43 44 41 46C39.7 47.3 39 49 39 51" stroke="black" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
    </div>

    <nav class="w-full max-w-7xl mx-auto px-8 py-10 flex justify-between items-center z-50">
        <div class="text-3xl font-extrabold italic tracking-tighter text-slate-900">K-Brain</div>
        <div class="flex items-center space-x-8">
            <a href="https://www.instagram.com/ksnk.hjm3/" target="_blank" class="text-[11px] font-bold text-slate-400 hover:text-sky-500 uppercase tracking-[0.2em] transition">Instagram</a>
            <a href="https://ksnk-brain.jp" class="px-7 py-3 bg-slate-900 text-white text-[11px] font-bold rounded-full hover:bg-sky-600 transition tracking-widest uppercase">Launch Engine</a>
        </div>
    </nav>

    <main class="flex-grow flex flex-col items-center justify-center px-6 text-center">
        <div class="inline-flex items-center space-x-2 px-4 py-1.5 mb-10 bg-white border border-slate-100 rounded-full shadow-sm">
            <span class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-sky-500"></span>
            </span>
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Nexus Project v22.3</span>
        </div>
        
        <h1 class="hero-title text-7xl md:text-9xl font-extrabold mb-10">
            視点が重なるとき、<br>臨床は変わる。
        </h1>
        
        <p class="text-xl md:text-2xl text-slate-400 font-light mb-16 leading-relaxed max-w-3xl">
            理学療法と看護の知能を統合。<br class="hidden md:block">
            16万件のエビデンスから、チーム医療の根拠を1秒で。
        </p>

        <div class="w-full max-w-3xl search-card p-2">
            <form action="/search" method="GET" class="flex items-center">
                <input type="text" name="q" placeholder="疾患、手技、論文タイトルを解析..." 
                       class="flex-grow bg-transparent px-8 py-6 text-xl focus:outline-none placeholder-slate-300">
                <button type="submit" class="btn-premium px-10 py-5 text-white rounded-[1.8rem] font-extrabold tracking-widest uppercase text-sm">
                    Analyze
                </button>
            </form>
        </div>

        <div class="mt-12 flex flex-wrap justify-center gap-3">
            <button onclick="location.href='/search?q=心不全リハ'" class="px-6 py-2.5 bg-white border border-slate-200 rounded-full text-[11px] font-bold text-slate-400 hover:border-sky-300 hover:text-sky-500 transition shadow-sm uppercase tracking-wider">心不全リハ</button>
            <button onclick="location.href='/search?q=夜間せん妄'" class="px-6 py-2.5 bg-white border border-slate-200 rounded-full text-[11px] font-bold text-slate-400 hover:border-sky-300 hover:text-sky-500 transition shadow-sm uppercase tracking-wider">夜間せん妄</button>
            <button onclick="location.href='/search?q=BPSD対応'" class="px-6 py-2.5 bg-white border border-slate-200 rounded-full text-[11px] font-bold text-slate-400 hover:border-sky-300 hover:text-sky-500 transition shadow-sm uppercase tracking-wider">BPSD対応</button>
        </div>
    </main>

    <footer class="py-12 text-center">
        <div class="text-[10px] text-slate-300 tracking-[0.4em] font-bold uppercase">
            &copy; 2026 K-BRAIN NEXUS PROJECT | MEDICAL INTELLIGENCE ARCHIVE
        </div>
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return render_template_string(INDEX_HTML)
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT title, abstract, url, source FROM papers WHERE title ILIKE %s OR abstract ILIKE %s ORDER BY id DESC LIMIT 50", (f'%{query}%', f'%{query}%'))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # 結果画面もミニマルなテイストに
        results_html = f'''
        <body style="background:#ffffff; color:#101828; font-family:sans-serif; padding:60px 20px;">
            <div style="max-width:900px; margin:0 auto;">
                <header style="margin-bottom:60px; text-align:center;">
                    <a href="/" style="text-decoration:none; color:#98a2b3; font-size:11px; font-weight:bold; letter-spacing:0.2em; text-transform:uppercase;">← Back to Command</a>
                    <h2 style="font-size:48px; font-weight:800; margin-top:24px; letter-spacing:-0.02em;">Search Results for "{query}"</h2>
                    <p style="color:#98a2b3; font-size:14px; font-weight:400; text-transform:uppercase; letter-spacing:0.1em; margin-top:8px;">16萬件の知能アーカイブから抽出</p>
                </header>
                {"".join([f'<div style="background:white; padding:40px; border-radius:32px; margin-bottom:32px; border:1px solid #f2f4f7; box-shadow:0 10px 30px rgba(0,0,0,0.02);"> <strong style="display:block; font-size:22px; line-height:1.4; margin-bottom:16px; color:#101828;">{r[0]}</strong> <p style="font-size:16px; color:#475467; line-height:1.7; margin-bottom:24px;">{r[1] or "詳細データは外部リンクを確認してください。"}</p> <a href="{r[2]}" target="_blank" style="display:inline-block; padding:12px 24px; background:#f9fafb; color:#0ea5e9; font-size:12px; font-weight:bold; text-decoration:none; border-radius:12px;">OPEN EVIDENCE →</a> </div>' for r in rows])}
            </div>
        </body>
        '''
        return results_html
    except Exception as e:
        return f"Database Connection Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
