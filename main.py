import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [設定エリア] ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# --- [デザイン：基の絵を完全に中心へ据えた、静寂と知性のデザイン] ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078" crossorigin="anonymous"></script>
    <title>K-Brain | 臨床知能アーカイブ</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Noto+Sans+JP:wght@300;500;700&display=swap');
        
        body { 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            background-color: #fafafa; /* わずかに温かみのある白（紙の質感に近い） */
            color: #1a1a1a;
            overflow-x: hidden;
        }

        /* 💡 先生の「基の絵」を再現した背景ロゴ */
        .art-background {
            position: fixed;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;
            max-width: 550px;
            z-index: -1;
            opacity: 0.15; /* ちょうど良い「透かし」具合 */
            filter: blur(0.5px);
        }

        .hero-title {
            letter-spacing: -0.06em;
            line-height: 1.1;
            font-weight: 800;
            color: #1a1a1a;
        }

        /* 🎨 Readdy風：浮遊する超ミニマルな検索バー */
        .search-pill {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 0, 0, 0.05);
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.05);
            border-radius: 9999px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .search-pill:focus-within {
            transform: translateY(-4px);
            box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.1);
            border-color: #B9D4DB;
        }

        .btn-analyze {
            background-color: #A3C9D6; /* 十字架のあの水色 */
            color: white;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(163, 201, 214, 0.3);
        }

        .btn-analyze:hover {
            background-color: #8bb6c5;
            transform: scale(1.02);
        }

        .nav-link {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.2em;
            color: #a0a0a0;
            text-transform: uppercase;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-background">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect x="38" y="10" width="24" height="80" rx="12" fill="#A3C9D6" />
            <rect x="10" y="38" width="80" height="24" rx="12" fill="#A3C9D6" />
            <path d="M50 85 C50 70 52 50 58 30" stroke="#1a1a1a" stroke-width="1.2" fill="none" stroke-linecap="round"/>
            <path d="M53 65 C58 60 65 55 68 45" stroke="#1a1a1a" stroke-width="1" fill="none" stroke-linecap="round"/>
            <path d="M54 50 C60 45 68 40 70 30" stroke="#1a1a1a" stroke-width="1" fill="none" stroke-linecap="round"/>
            <path d="M48 60 C42 62 35 68 32 75" stroke="#1a1a1a" stroke-width="1" fill="none" stroke-linecap="round"/>
            <path d="M47 45 C40 48 32 55 30 65" stroke="#1a1a1a" stroke-width="1" fill="none" stroke-linecap="round"/>
            <circle cx="68" cy="45" r="1.5" fill="#1a1a1a"/>
            <circle cx="70" cy="30" r="1.5" fill="#1a1a1a"/>
            <circle cx="32" cy="75" r="1.5" fill="#1a1a1a"/>
            <circle cx="30" cy="65" r="1.5" fill="#1a1a1a"/>
        </svg>
    </div>

    <header class="w-full max-w-7xl px-10 py-12 flex justify-between items-center z-50">
        <div class="text-3xl font-extrabold italic tracking-tighter">K-Brain</div>
        <div class="flex items-center space-x-10">
            <a href="https://www.instagram.com/ksnk.hjm3/" target="_blank" class="nav-link hover:text-slate-900 transition">Instagram</a>
            <a href="https://ksnk-brain.jp" class="px-8 py-3 bg-slate-900 text-white text-[10px] font-bold rounded-full tracking-widest uppercase hover:bg-sky-600 transition">Launch System</a>
        </div>
    </header>

    <main class="flex-grow flex flex-col items-center justify-center px-6 text-center w-full">
        <div class="mb-6 py-1 px-4 border border-slate-200 rounded-full inline-block">
            <span class="text-[9px] font-bold text-slate-400 tracking-[0.3em] uppercase">Clinical Intelligence Nexus</span>
        </div>
        
        <h1 class="hero-title text-6xl md:text-8xl mb-10">
            視点が重なるとき、<br>臨床は変わる。
        </h1>
        
        <p class="text-lg md:text-xl text-slate-400 font-light mb-16 max-w-2xl leading-relaxed">
            理学療法と看護の知能を統合。<br>
            16万件のエビデンスから、チーム医療の根拠を1秒で。
        </p>

        <div class="w-full max-w-3xl search-pill p-2">
            <form action="/search" method="GET" class="flex items-center">
                <input type="text" name="q" placeholder="キーワードを解析..." 
                       class="flex-grow bg-transparent px-8 py-5 text-xl focus:outline-none placeholder-slate-200">
                <button type="submit" class="btn-analyze px-12 py-5 rounded-full font-extrabold tracking-widest uppercase text-sm">
                    Analyze
                </button>
            </form>
        </div>

        <div class="mt-12 flex space-x-4">
            <button onclick="location.href='/search?q=心不全リハ'" class="text-[10px] font-bold text-slate-300 hover:text-sky-400 transition tracking-widest uppercase">#HeartFailure</button>
            <button onclick="location.href='/search?q=夜間せん妄'" class="text-[10px] font-bold text-slate-300 hover:text-sky-400 transition tracking-widest uppercase">#Delirium</button>
        </div>
    </main>

    <footer class="py-12">
        <div class="text-[9px] text-slate-300 tracking-[0.5em] font-bold uppercase">
            &copy; 2026 K-BRAIN NEXUS PROJECT | EVIDENCE BASED MEDICINE
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

        results_html = f'''
        <body style="background:#fafafa; color:#1a1a1a; font-family:sans-serif; padding:60px 20px;">
            <div style="max-width:900px; margin:0 auto;">
                <header style="margin-bottom:60px; text-align:center;">
                    <a href="/" style="text-decoration:none; color:#d1d1d1; font-size:10px; font-weight:bold; letter-spacing:0.3em; text-transform:uppercase;">← Command Center</a>
                    <h2 style="font-size:42px; font-weight:800; margin-top:24px; letter-spacing:-0.03em;">Search: {query}</h2>
                </header>
                {"".join([f'<div style="background:white; padding:40px; border-radius:40px; margin-bottom:32px; box-shadow:0 20px 40px rgba(0,0,0,0.03); border:1px solid rgba(0,0,0,0.02);"> <strong style="display:block; font-size:22px; line-height:1.4; margin-bottom:16px;">{r[0]}</strong> <p style="font-size:16px; color:#777; line-height:1.8; margin-bottom:24px;">{r[1] or "詳細データは外部リンクを確認してください。"}</p> <a href="{r[2]}" target="_blank" style="display:inline-block; padding:12px 28px; background:#A3C9D6; color:white; font-size:11px; font-weight:bold; text-decoration:none; border-radius:99px; letter-spacing:0.1em;">GET EVIDENCE</a> </div>' for r in rows])}
            </div>
        </body>
        '''
        return results_html
    except Exception as e:
        return f"Database Connection Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
