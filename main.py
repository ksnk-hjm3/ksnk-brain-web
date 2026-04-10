import os
import re
import hashlib
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from flask import Flask, request, render_template_string
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# --- [1. データベース設定：接続先を hajime に固定] ---
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/hajime")
pool = SimpleConnectionPool(1, 10, dsn=DATABASE_URL)

CACHE = {}

def query_db(sql, params=None):
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        pool.putconn(conn)

# --- [2. 検索知能：ハイブリッド・スコアリング] ---
def get_embedding(text):
    return client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding

def search(query):
    embedding = get_embedding(query)
    # 検索精度：FTS(40%) + Vector(60%)。NULL安全性を高めたSQL。
    sql = """
    SELECT id, title, abstract, url,
           ts_rank_cd(to_tsvector('english', title || ' ' || COALESCE(abstract,'')), plainto_tsquery('english', %s)) AS fts_score,
           1 - (embedding <=> %s::vector) AS vec_score
    FROM papers
    WHERE embedding IS NOT NULL
    ORDER BY (fts_score * 0.4 + vec_score * 0.6) DESC
    LIMIT 12;
    """
    return query_db(sql, (query, embedding, query))

# --- [3. エビデンス・グレーディング] ---
def detect_study_design(text):
    t = (text or "").lower()
    if any(k in t for k in ["meta-analysis", "systematic review"]): return "Meta-analysis"
    if "randomized" in t: return "RCT"
    if "cohort" in t: return "Cohort Study"
    if "case report" in t: return "Case Report"
    return "Clinical Evidence"

# --- [4. 臨床意思決定：The Nexus 推論ロジック] ---
def generate_decision(query, rows):
    evidence_payload = ""
    for i, r in enumerate(rows):
        design = detect_study_design(r[2])
        evidence_payload += f"[{i+1}] ({design}) {r[1]}\\n{str(r[2])[:400]}\\n\\n"

    prompt = f"""
あなたは臨床推論パートナー「K-Brain」です。以下の学術的エビデンスを背景に、臨床的な意思決定を支援せよ。

【臨床課題】
{query}

【エビデンス】
{evidence_payload}

---
【厳守ルール】
1. 必ず引用番号[1]を使用し、存在しない情報は書かない。
2. エビデンス間の「矛盾」がある場合は、臨床的な安全策を優先して提示せよ。
3. リハと看護、異なる専門性が現場で「共通言語」として使えるように解析せよ。

【出力構成】
■ 【Summary】
エビデンスに基づく結論（引用番号付き）

■ 【Decision Guide】
1. 第一選択（推奨される介入）
2. 個別配慮・代替案
3. Red Flags（避けるべき、または中止すべき基準）

■ 【The Nexus Insight】
理学療法士と看護師がベッドサイドで共有すべき「観察の視点」と「具体的声かけ」。

■ 【Evidence Quality】
信頼性評価（高/中/低）と、エビデンスがカバーしきれない「限界」。
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a professional clinical strategist."},
                  {"role": "user", "content": prompt}],
        temperature=0.1
    )
    return res.choices[0].message.content

# --- [5. UIデザイン：臨床の聖域を再現] ---
HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain Nexus</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+JP:wght@100;400;700;900&display=swap');
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: #fafafa; color: #1a1a1a; }
        .watercolor-bg {
            position: fixed; top: 48%; left: 50%; transform: translate(-50%, -50%);
            width: 95%; max-width: 550px; z-index: -1; pointer-events: none;
            filter: drop-shadow(0 0 20px rgba(163, 201, 214, 0.2));
        }
        .glass-panel { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); border-radius: 48px; border: 1px solid rgba(0,0,0,0.03); }
        .marker { background: linear-gradient(180deg, transparent 70%, rgba(163, 201, 214, 0.3) 70%); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center">

    <div class="watercolor-bg">
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M38.5 10C38.5 8 40.5 6 42.5 6H57.5C59.5 6 61.5 8 61.5 10V38.5H90C92 38.5 94 40.5 94 42.5V57.5C94 59.5 92 61.5 90 61.5H61.5V90C61.5 92 59.5 94 57.5 94H42.5C40.5 94 38.5 92 38.5 90V61.5H10C8 61.5 6 59.5 6 57.5V42.5C6 40.5 8 38.5 10 38.5H38.5V10Z" fill="#A3C9D6" fill-opacity="0.85"/>
            <path d="M52 88 C52 75 54 52 60 35" stroke="#1a1a1a" stroke-width="1.3" stroke-linecap="round"/>
            <path d="M55 65 C60 60 68 55 72 45" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M57 48 C64 43 72 38 75 28" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M48 68 C42 70 34 76 30 85" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M47 50 C40 53 30 62 28 72" stroke="#1a1a1a" stroke-width="0.9" stroke-linecap="round"/>
            <path d="M72 45 Q74 43 73.5 46.5 Q73 50 71 45.5 Z" fill="#1a1a1a"/>
            <path d="M75 28 Q77 26 76.5 29.5 Q76 33 74 28.5 Z" fill="#1a1a1a"/>
            <path d="M30 85 Q28 87 28.5 83.5 Q29 80 31 84.5 Z" fill="#1a1a1a"/>
            <path d="M28 72 Q26 74 26.5 70.5 Q27 67 29 71.5 Z" fill="#1a1a1a"/>
        </svg>
    </div>

    <header class="w-full max-w-6xl px-8 py-12 flex justify-between items-center z-50">
        <div class="text-3xl font-black italic tracking-tighter text-slate-950">K-Brain <span class="text-sky-500">Nexus</span></div>
        <a href="https://ksnk-brain.jp" class="px-7 py-3 bg-slate-950 text-white text-[11px] font-bold rounded-full uppercase tracking-tighter shadow-xl">Launch System</a>
    </header>

    <main class="w-full max-w-6xl px-4 flex flex-col items-center">
        <div class="w-full max-w-2xl mb-20 px-2">
            <form action="/search" class="bg-white rounded-full shadow-2xl flex items-center p-2 border border-slate-50">
                <input name="q" value="{{q}}" class="flex-grow pl-6 pr-2 py-4 text-lg outline-none bg-transparent" placeholder="臨床課題を入力...">
                <button class="bg-[#A3C9D6] text-white px-10 py-4 rounded-full font-bold shadow-md hover:bg-sky-400 transition-all">解析 🔍</button>
            </form>
        </div>

        {% if summary %}
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-10 w-full mb-40">
            <div class="lg:col-span-2 glass-panel p-12 shadow-sm">
                <div class="text-[10px] font-bold text-sky-600 uppercase mb-8 tracking-[0.3em]">Clinical Intelligence Report</div>
                <div class="prose prose-slate max-w-none text-slate-700 leading-relaxed whitespace-pre-wrap">{{summary}}</div>
            </div>
            <div class="lg:col-span-1 space-y-6">
                <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-4">Supporting Evidence</div>
                {% for e in evidence %}
                <div class="bg-white/60 p-6 rounded-[32px] border border-white shadow-sm hover:shadow-md transition-all">
                    <div class="text-[9px] font-bold text-sky-500 mb-2 uppercase">[{ {e.id} }] {{e.type}}</div>
                    <h3 class="font-bold text-sm text-slate-800 mb-3 line-clamp-2">{{e.title}}</h3>
                    <a href="{{e.url}}" target="_blank" class="text-[10px] font-bold text-slate-300 hover:text-sky-500 uppercase">View on PubMed →</a>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </main>

    <footer class="w-full py-16 bg-white/50 border-t border-slate-100 text-center text-[10px] text-slate-300 font-bold tracking-[0.5em] uppercase">
        &copy; 2026 K-BRAIN NEXUS PROJECT | EBM INTELLIGENCE
    </footer>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, q="", summary=None, evidence=[])

@app.route("/search")
def run():
    q = request.args.get("q", "").strip()
    if not q: return index()

    key = hashlib.md5(q.encode()).hexdigest()
    if key in CACHE: return render_template_string(HTML, q=q, **CACHE[key])

    rows = search(q)
    # 昇華ポイント：構造化データの生成
    evidence = [{"id": i+1, "title": r[1], "url": r[3], "type": detect_study_design(r[2])} for i, r in enumerate(rows)]
    summary = generate_decision(q, rows)

    result = {"summary": summary, "evidence": evidence}
    CACHE[key] = result
    return render_template_string(HTML, q=q, **result)

if __name__ == "__main__":
    # Renderのポート番号に自動対応
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
