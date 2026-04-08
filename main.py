import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [設定エリア] ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# --- [デザイン：Readdy AI の質感と基の絵の完全融合] ---
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
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,600;0,800;1,800&family=Noto+Sans+JP:wght@300;400;700&display=swap');
        
        :root {
            --bg-color: #fafafa;
            --accent-blue: #A3C9D6;
            --text-main: #1a1a1a;
            --text-sub: #8e8e93;
        }

        body { 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            background-color: var(--bg-color); 
            color: var(--text-main);
            overflow-x: hidden;
        }

        /* 🌳 「基の絵」を完全に中心へ。水彩のような透明感を再現 */
        .art-core {
            position: fixed;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 85%;
            max-width: 600px;
            z-index: -1;
            opacity: 0.12;
            filter: blur(0.4px);
            pointer-events: none;
        }

        /* Readdy風：タイポグラフィの強弱 */
        .hero-title {
            font-size: clamp(3rem, 8vw, 6rem);
            font-weight: 800;
            letter-spacing: -0.05em;
            line-height: 1.05;
            margin-bottom: 2.5rem;
        }

        .hero-sub {
            font-size: clamp(1rem, 2vw, 1.25rem);
            font-weight: 300;
            color: var(--text-sub);
            line-height: 1.8;
            letter-spacing: 0.02em;
        }

        /* Readdy風：洗練された検索フィールド */
        .input-pill {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 0, 0, 0.04);
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.03);
            border-radius: 100px;
            transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .input-pill:focus-within {
            transform: translateY(-2px);
            background: #ffffff;
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.08);
            border-color: var(--accent-blue);
        }

        .btn-analyze {
            background: var(--accent-blue);
            color: white;
            border-radius: 100px;
            font-weight: 700;
            letter-spacing: 0.1em;
            transition: all 0.3s ease;
        }

        .btn-analyze:hover {
            transform: scale(1.03);
            filter: brightness(1.05);
            box-shadow: 0 10px 20px rgba(163, 201, 214, 0.3);
        }

        /* Readdy風：ナビゲーションの潔さ */
        .nav-link {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            color: var(--text-sub);
            transition: color 0.3s;
        }

        .nav-link:hover { color: var(--text-main); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-core">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect x="39" y="8" width="22" height="84" rx="11" fill="var(--accent-blue)" />
            <rect x="8" y="39" width="84" height="22" rx="11" fill="var(--accent-blue)" />
            <path d="M50 88 C50 72 52 55 58 35" stroke="#1a1a1a" stroke-width="1.2" fill="none" stroke-linecap="round"/>
            <path d="M53 68 C58 63 65 58 68 48" stroke="#1a1a1a" stroke-width="0.8" fill="none" stroke-linecap="round"/>
            <path d="M54 53 C60 48 68 43 70 33" stroke="#1a1a1a" stroke-width="0.8" fill="none" stroke-linecap="round"/>
            <path d="M48 63 C42 65 35 71 32 78" stroke="#1a1a1a" stroke-width="0.8" fill="none" stroke-linecap="round"/>
            <path d="M47 48 C40 51 32 58 30 68" stroke="#1a1a1a" stroke-width="0.8" fill="none" stroke-linecap="round"/>
            <circle cx="68" cy="48" r="1.2" fill="#1a1a1a"/>
            <circle cx="70" cy="33" r="1.2" fill="#1a1a1a"/>
            <circle cx="32" cy="78" r="1.2" fill="#1a1a1a"/>
            <circle cx="30" cy="68" r="1.2" fill="#1a1a1a"/>
        </svg>
    </div>

    <header class="w-full max-w-7xl px-12 py-16 flex justify-between items-center z-50">
        <div class="text-3xl font-extrabold italic tracking-tighter">K-Brain</div>
        <nav class="flex items-center space-x-12">
            <a href="https://www.instagram.com/ksnk.hjm3/" target="_blank" class="nav-link">Instagram</a>
            <a href="https://ksnk-brain.jp" class="px-8 py-3 bg-black text-white text-[10px] font-bold rounded-full tracking-[0.2em] uppercase hover:bg-zinc-800 transition">Launch System</a>
        </nav>
    </header>

    <main class="flex-grow flex flex-col items-center justify-center px-8 text-center w-full max-w-5xl">
        <div class="mb-10 py-1 px-4 border border-zinc-200 rounded-full inline-block">
            <span class="text-[9px] font-bold text-zinc-400 tracking-[0.4em] uppercase">Academic Insight Nexus</span>
        </div>
        
        <h1 class="hero-title">
            視点が重なるとき、<br>臨床は変わる。
        </h1>
        
        <p class="hero-sub mb-20 max-w-3xl">
            リハビリテーションと看護の視点が重なる場所に。<br>
            16万件の学術データから、チーム医療の揺るぎない共通言語を。
        </p>

        <div class="w-full max-w-3xl input-pill p-2 flex items-center">
            <form action="/search" method="GET" class="flex w-full items-center">
                <input type="text" name="q" placeholder="臨床課題をキーワードで検索..." 
                       class="flex-grow bg-transparent px-8 py-5 text-xl outline-none placeholder-zinc-300">
                <button type="submit" class="btn-analyze px-12 py-5 uppercase text-xs">
                    Analyze
                </button>
            </form>
        </div>

        <div class="mt-16 flex space-x-8">
            <button onclick="location.href='/search?q=心不全リハ'" class="text-[10px] font-bold text-zinc-300 hover:text-zinc-900 transition tracking-[0.3em] uppercase">#CardiacRehab</button>
            <button onclick="location.href='/search?q=夜間せん妄'" class="text-[10px] font-bold text-zinc-300 hover:text-zinc-900 transition tracking-[0.3em] uppercase">#DeliriumCare</button>
        </div>
    </main>

    <footer class="py-16">
        <div class="text-[9px] text-zinc-300 tracking-[0.6em] font-bold uppercase">
            &copy; 2026 K-BRAIN NEXUS PROJECT | EBM ARCHIVE
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

        # 結果画面も徹底的にミニマル化
        results_html = f'''
        <body style="background:#fafafa; color:#1a1a1a; font-family:'Inter', sans-serif; padding:80px 40px;">
            <div style="max-width:840px; margin:0 auto;">
                <header style="margin-bottom:80px; text-align:center;">
                    <a href="/" style="text-decoration:none; color:#d1d1d1; font-size:10px; font-weight:700; letter-spacing:0.4em; text-transform:uppercase;">← Command Center</a>
                    <h2 style="font-size:42px; font-weight:800; margin-top:32px; letter-spacing:-0.04em;">Results: {query}</h2>
                </header>
                {"".join([f'<div style="background:white; padding:48px; border-radius:48px; margin-bottom:40px; box-shadow:0 30px 60px -20px rgba(0,0,0,0.04); border:1px solid rgba(0,0,0,0.01);"> <strong style="display:block; font-size:24px; line-height:1.35; margin-bottom:20px; font-weight:800; letter-spacing:-0.02em;">{r[0]}</strong> <p style="font-size:17px; color:#666; line-height:1.8; margin-bottom:32px; font-weight:300;">{r[1] or "詳細データは外部リンクを確認してください。"}</p> <a href="{r[2]}" target="_blank" style="display:inline-block; padding:16px 32px; background:#A3C9D6; color:white; font-size:11px; font-weight:800; text-decoration:none; border-radius:100px; letter-spacing:0.15em; text-transform:uppercase;">Open Evidence</a> </div>' for r in rows])}
            </div>
        </body>
        '''
        return results_html
    except Exception as e:
        return f"Database Connection Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
