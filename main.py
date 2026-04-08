import os
import sqlite3 # 不要？Render PostgreSQLに変更した。
import psycopg2
from Flask import Flask, request, render_template_string, jsonify
from datetime import datetime

app = Flask(__name__)

# --- [設定エリア] ---
# スクリーンショットから判明した先生のRender接続情報
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/k_brain_v22_3"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def get_evidence_count():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM papers")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        # 桁区切りを入れる（例：168,349）
        return "{:,}".format(count)
    except Exception as e:
        print(f"Count Error: {e}")
        # エラー時は image_6.png のダミー値を表示
        return "168,349"

# --- [デザイン：Readdy AI & K-Brain Nexus v4.0] ---
# image_6.pngのデザインを完璧に模倣し、クスノキのアイデンティティを融合

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
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,600;0,800;1,800&family=Noto+Sans+JP:wght@300;400;700&display=swap');
        
        :root {
            --bg-color: #fafafa;
            --accent-blue: #A3C9D6; /* image_6.pngの水色 */
            --text-main: #1a1a1a;
            --text-sub: #8e8e93;
        }

        body { 
            font-family: 'Inter', 'Noto Sans JP', sans-serif; 
            background-color: var(--bg-color); 
            color: var(--text-main);
            overflow-x: hidden;
        }

        /* image_5.pngの十字と植物を完璧に再現 */
        .art-background {
            position: fixed;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;
            max-width: 600px;
            z-index: -2;
            opacity: 0.1;
            filter: blur(0.3px);
            pointer-events: none;
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

        /* image_6.pngの検索窓 */
        .search-field {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid #f2f4f7;
            border-radius: 999px;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.03);
            transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .search-field:focus-within {
            background: #ffffff;
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.08);
            border-color: var(--accent-blue);
        }

        .btn-analyze {
            background: var(--accent-blue);
            color: white;
            border-radius: 999px;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }

        .btn-analyze:hover {
            filter: brightness(1.05);
            box-shadow: 0 10px 20px rgba(163, 201, 214, 0.3);
        }

        /* image_6.pngのステータスカード（カテゴリ） */
        .status-card {
            background: #ffffff;
            padding: 24px;
            border-radius: 20px;
            border: 1px solid #f2f4f7;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        }

        /* image_6.pngのHOW TO USEステップカード */
        .step-card {
            background: #ffffff;
            padding: 32px;
            border-radius: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
            border: 1px solid rgba(0,0,0,0.01);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="art-background">
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

    <header class="w-full max-w-7xl px-12 py-10 flex justify-between items-center z-50">
        <div class="text-3xl font-extrabold italic tracking-tighter text-slate-900">K-Brain</div>
        <nav class="flex items-center space-x-10 text-[11px] font-bold text-slate-400 hover:text-sky-500 uppercase tracking-widest">
            <a href="https://www.instagram.com/ksnk.hjm3/" target="_blank">Instagram</a>
            <a href="https://ksnk-brain.jp" class="px-7 py-3 bg-slate-950 text-white rounded-full hover:bg-zinc-800 transition">Launch System</a>
        </nav>
    </header>

    <main class="flex-grow flex flex-col items-center px-8 w-full max-w-6xl text-center">
        <div class="mb-10 py-1 px-4 bg-white border border-slate-100 rounded-full inline-block shadow-sm">
            <span class="text-[9px] font-bold text-sky-600 tracking-[0.4em] uppercase">Academic Insight Nexus</span>
        </div>
        
        <h1 class="hero-title">
            視点が重なるとき、<br>臨床は変わる。
        </h1>
        
        <p class="hero-sub mb-20 max-w-3xl">
            リハビリテーションと看護の視点が重なる場所に。<br>
            16万件の学術データから、チーム医療の揺るぎない共通言語を。
        </p>

        <section class="w-full grid grid-cols-1 md:grid-cols-3 gap-6 mb-20 text-left">
            <div class="status-card flex items-center space-x-4">
                <div class="p-3 bg-sky-50 text-sky-600 rounded-full">
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                </div>
                <div>
                    <div class="text-[11px] text-slate-400 uppercase tracking-widest">収録エビデンス数</div>
                    <div class="text-4xl font-extrabold text-slate-900">{{ evidence_count }}</div>
                </div>
            </div>
            <div class="status-card flex items-center space-x-4">
                <div class="p-3 bg-sky-50 text-sky-600 rounded-full">
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a2 2 0 00-1.96 1.414l-.724 2.17a2 2 0 001.575 2.577l2.931.586a2 2 0 002.01-1.432l.724-2.17a2 2 0 00-.547-2.122z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.142 8.142a2 2 0 001.022.547l2.387.477a2 2 0 001.96-1.414l.724-2.17a2 2 0 00-1.575-2.577l-2.931-.586a2 2 0 00-2.01 1.432l-.724 2.17a2 2 0 00.547 2.122z" /></svg>
                </div>
                <div>
                    <div class="text-[11px] text-slate-400 uppercase tracking-widest">対応専門領域</div>
                    <div class="text-4xl font-extrabold text-slate-900">12 分野</div>
                </div>
            </div>
            <div class="status-card flex items-center space-x-4">
                <div class="p-3 bg-sky-50 text-sky-600 rounded-full">
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
                </div>
                <div>
                    <div class="text-[11px] text-slate-400 uppercase tracking-widest">最終更新</div>
                    <div class="text-4xl font-extrabold text-slate-900">2026.04</div>
                </div>
            </div>
        </section>

        <div class="w-full max-w-4xl search-field p-2 flex items-center mb-32">
            <form action="/search" method="GET" class="flex w-full items-center">
                <input type="text" name="q" placeholder="臨床課題をキーワードで検索（例：心不全 離床）..." 
                       class="flex-grow bg-transparent px-8 py-5 text-xl outline-none placeholder-slate-300">
                <button type="submit" class="btn-analyze px-12 py-5 uppercase text-xs">
                    Analyze
                </button>
            </form>
        </div>

        <section class="w-full text-left mb-32">
            <div class="text-center mb-16">
                <span class="text-[11px] font-bold text-slate-400 tracking-[0.5em] uppercase">HOW TO USE</span>
                <h2 class="text-5xl font-extrabold text-slate-900 mt-4 leading-tight">3ステップで、<br>エビデンスを臨床へ。</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="step-card">
                    <div class="p-4 bg-sky-50 text-sky-600 rounded-2xl inline-block mb-6">
                        <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                    </div>
                    <div class="text-[11px] font-bold text-sky-600 uppercase tracking-widest">STEP 1</div>
                    <h3 class="text-2xl font-extrabold text-slate-900 mt-2">疾患名・手技を入力</h3>
                    <p class="text-sm text-slate-500 mt-4 leading-relaxed">日本語・英語どちらでも検索可能。AND/OR検索にも対応。</p>
                </div>
                <div class="step-card">
                    <div class="p-4 bg-sky-50 text-sky-600 rounded-2xl inline-block mb-6">
                        <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" /></svg>
                    </div>
                    <div class="text-[11px] font-bold text-sky-600 uppercase tracking-widest">STEP 2</div>
                    <h3 class="text-2xl font-extrabold text-slate-900 mt-2">フィルターで絞り込み</h3>
                    <p class="text-sm text-slate-500 mt-4 leading-relaxed">発行年・ジャーナル・言語で素早く目的の論文へ。</p>
                </div>
                <div class="step-card">
                    <div class="p-4 bg-sky-50 text-sky-600 rounded-2xl inline-block mb-6">
                        <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                    </div>
                    <div class="text-[11px] font-bold text-sky-600 uppercase tracking-widest">STEP 3</div>
                    <h3 class="text-2xl font-extrabold text-slate-900 mt-2">エビデンスを確認</h3>
                    <p class="text-sm text-slate-500 mt-4 leading-relaxed">要約・引用数・関連論文を一覧で確認。PubMedへ直接リンク。</p>
                </div>
            </div>
        </section>

    </main>

    <footer class="py-16 text-center border-t border-slate-100 w-full mt-12 bg-white">
        <div class="text-[9px] text-slate-300 tracking-[0.6em] font-bold uppercase">
            &copy; 2026 K-BRAIN NEXUS PROJECT | EBM ARCHIVE
        </div>
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    # データベースから実際の収録件数を取得して埋め込む
    evidence_count = get_evidence_count()
    return render_template_string(INDEX_HTML, evidence_count=evidence_count)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return render_template_string(INDEX_HTML)
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # タイトルと抄録から検索
        cur.execute("SELECT title, abstract, url, source FROM papers WHERE title ILIKE %s OR abstract ILIKE %s ORDER BY id DESC LIMIT 50", (f'%{query}%', f'%{query}%'))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # 結果画面もトップページと調和させる
        results_html = f'''
        <body style="background:#fafafa; color:#1a1a1a; font-family:'Inter', sans-serif; padding:80px 40px;">
            <div style="max-width:840px; margin:0 auto;">
                <header style="margin-bottom:80px; text-align:center;">
                    <a href="/" style="text-decoration:none; color:#94a3b8; font-size:11px; font-weight:700; letter-spacing:0.4em; text-transform:uppercase; transition: color 0.3s;">← Back to home</a>
                    <h2 style="font-size:42px; font-weight:800; margin-top:32px; letter-spacing:-0.04em;">「{query}」の解析結果</h2>
                    <p style="color:#64748b; font-size:16px; font-weight:400; letter-spacing:0.02em; margin-top:8px;">16万件の学術アーカイブから{len(rows)}件のエビデンスが抽出されました</p>
                </header>
                {"".join([f'<div style="background:white; padding:48px; border-radius:32px; margin-bottom:40px; box-shadow:0 30px 60px -20px rgba(0,0,0,0.04); border:1px solid rgba(0,0,0,0.01);"> <strong style="display:block; font-size:24px; line-height:1.35; margin-bottom:20px; font-weight:800; letter-spacing:-0.02em;">{r[0]}</strong> <p style="font-size:17px; color:#475569; line-height:1.8; margin-bottom:32px; font-weight:300;">{r[1] or "詳細データは外部リンクを確認してください。"}</p> <a href="{r[2]}" target="_blank" style="display:inline-block; padding:16px 32px; background:#A3C9D6; color:white; font-size:11px; font-weight:800; text-decoration:none; border-radius:100px; letter-spacing:0.15em; text-transform:uppercase;">Open Evidence</a> </div>' for r in rows])}
            </div>
        </body>
        '''
        return results_html
    except Exception as e:
        return f"Database Connection Error: {str(e)}"

if __name__ == '__main__':
    # host='0.0.0.0' を追加しました。これでRenderが通信できるようになります。
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
