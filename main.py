import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- [設定エリア] ---
# スクリーンショットから取得した先生専用のDB接続情報
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# --- [デザイン：Readdy AI & K-Brain Nexus v4.0] ---
# image_1.pngのテイストを目指しつつ、スマホ（image_7.png）での崩れを修正
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6734545930167078" crossorigin="anonymous"></script>
    <title>K-Brain | 臨床が変わる。破壊的な論理思考を。</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,600;0,800;1,800&family=Noto+Sans+JP:wght@300;400;700;800&display=swap');
        
        body { 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            background-color: #fafafa; /* Slate-50: 洗練されたライトグレー */
            color: #1a1a1a; 
            overflow-x: hidden;
        }

        /* 🌳 クスノキの透かし（中央に巨大かつ薄く配置） */
        .art-background {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%; /* 画面幅に対する比率 */
            max-width: 600px; /* PCでの最大幅 */
            z-index: -2;
            pointer-events: none;
            opacity: 0.1; /* 薄くする（好印象だった image_1.png のテイストに） */
        }

        /* Readdy風：タイポグラフィの強弱 */
        .hero-title {
            font-size: clamp(3rem, 7vw, 6rem);
            font-weight: 800;
            letter-spacing: -0.05em;
            line-height: 1.05;
            margin-bottom: 2.5rem;
            color: #101828;
        }

        .hero-sub {
            font-size: clamp(1rem, 2vw, 1.25rem);
            font-weight: 300;
            color: #475467;
            line-height: 1.8;
            letter-spacing: 0.02em;
        }

        /* Readdy風：洗練された検索フィールド */
        .search-field {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 0, 0, 0.05);
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.03);
            border-radius: 999px;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .search-field:focus-within {
            background: #ffffff;
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.08);
            border-color: #A3C9D6; /* 基の絵の水色 */
        }

        .btn-medical {
            background: #A3C9D6; /* 基の絵の水色 */
            color: white;
            border-radius: 999px;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            transition: all 0.2s ease;
        }

        .btn-medical:hover {
            transform: scale(1.02);
            filter: brightness(1.03);
        }

        /* 強調テキスト：破壊的な論理思考。スマホでの崩れを防ぐためパディング調整。 */
        .highlight-disruptive {
            font-weight: 700;
            color: #101828;
            background: linear-gradient(180deg, rgba(255,255,255,0) 60%, rgba(163, 201, 214, 0.2) 60%);
            display: inline-block;
            padding: 0 4px;
            margin: 0 -4px;
        }
        
        /* スマホでの窮屈さを解消するための余白設定 */
        @media (max-width: 640px) {
            .hero-title {
                margin-top: 10vh;
                margin-bottom: 3rem;
            }
            .hero-sub {
                margin-bottom: 4rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-background z-[-2]">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect x="39" y="8" width="22" height="84" rx="11" fill="#a3cfea" fill-opacity="0.8" />
            <rect x="8" y="39" width="84" height="22" rx="11" fill="#a3cfea" fill-opacity="0.8" />
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

    <header class="w-full max-w-7xl px-8 py-10 flex justify-between items-center z-50">
        <div class="text-3xl font-extrabold italic tracking-tighter text-slate-900">K-Brain</div>
        <div class="flex items-center space-x-10 text-[11px] font-bold text-slate-400 hover:text-sky-500 uppercase tracking-widest transition">
            <a href="https://www.instagram.com/ksnk.hjm3/" target="_blank">Instagram</a>
            <a href="https://ksnk-brain.jp" class="px-7 py-3 bg-slate-950 text-white rounded-full hover:bg-zinc-800 transition">Launch System</a>
        </div>
    </header>

    <main class="flex-grow flex flex-col items-center justify-center px-6 text-center w-full max-w-4xl hero-section">
        
        <h1 class="hero-title">
            臨床が変わる。
        </h1>
        
        <p class="hero-sub mb-16 max-w-2xl mx-auto text-left sm:text-center">
            リハビリテーションと看護の視点をひとつに。<br>
            膨大な学術データによる<span class="highlight-disruptive">「破壊的な論理思考」</span>を。
        </p>

        <div class="w-full max-w-3xl search-field p-2 flex items-center mb-16">
            <form action="/search" method="GET" class="flex w-full items-center">
                <input type="text" name="q" placeholder="疾患、手技、論文タイトルを解析..." 
                       class="flex-grow bg-transparent px-6 py-4 text-lg outline-none placeholder-slate-300">
                <button type="submit" class="btn-medical px-10 py-4 uppercase text-xs">
                    Analyze
                </button>
            </form>
        </div>

        <div class="flex space-x-6 text-[10px] font-bold text-slate-300 uppercase tracking-widest">
            <span>#HeartFailure</span>
            <span>#Delirium</span>
            <span>#Stroke</span>
        </div>
    </main>

    <footer class="w-full py-10 text-center border-t border-slate-100 bg-white">
        <div class="text-[9px] text-slate-300 tracking-[0.5em] font-bold uppercase">
            &copy; 2026 K-BRAIN NEXUS PROJECT | MEDICAL INTELLIGENCE
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

        # 結果画面もトップページと調和させる
        results_html = f'''
        <body style="background:#fafafa; color:#1a1a1a; font-family:sans-serif; padding:60px 20px;">
            <div style="max-width:900px; margin:0 auto;">
                <header style="margin-bottom:60px; text-align:center;">
                    <a href="/" style="text-decoration:none; color:#94a3b8; font-size:11px; font-weight:700; letter-spacing:0.4em; text-transform:uppercase; transition: color 0.3s;">← Back to Command</a>
                    <h2 style="font-size:42px; font-weight:800; margin-top:24px; letter-spacing:-0.03em;">Search: "{query}"</h2>
                </header>
                {"".join([f'<div style="background:white; padding:40px; border-radius:32px; margin-bottom:32px; border:1px solid #f2f4f7; box-shadow:0 10px 30px rgba(0,0,0,0.02);"> <strong style="display:block; font-size:20px; line-height:1.4; margin-bottom:16px;">{r[0]}</strong> <p style="font-size:16px; color:#475467; line-height:1.7; margin-bottom:24px;">{r[1] or "詳細データは外部リンクを確認してください。"}</p> <a href="{r[2]}" target="_blank" style="display:inline-block; padding:12px 24px; background:#fafafa; color:#A3C9D6; font-size:12px; font-weight:bold; text-decoration:none; border-radius:12px; border:1px solid #f1f5f9;">OPEN EVIDENCE →</a> </div>' for r in rows])}
            </div>
        </body>
        '''
        return results_html
    except Exception as e:
        return f"Database Connection Error: {str(e)}"

if __name__ == '__main__':
    # host='0.0.0.0' を追加しました。これでRenderが通信できるようになります。
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
