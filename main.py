import os, psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- 🚀 設定エリア ---
DATABASE_URL = "postgresql://hajime:0jsveDiLjj4VMsiqqKTYJaJFHmCC1PJr@dpg-d79ou6qdbo4c73afvnng-a.singapore-postgres.render.com/ksnk_brain"
ADMIN_NAME = "クスノキ"
INSTA_URL = "https://www.instagram.com/ksnk.hjm3/"

# 【重要】アドセンスから「このコードをheadに貼って」と言われたら、ここに貼り付けてください
# 審査前は空欄でOKです。
ADSENSE_HEAD_CODE = """
"""

# 【重要】広告を表示したい場所に貼る「広告ユニット」コード
ADS_UNIT_TOP = """<div style="text-align:center; margin:20px 0; color:#ccc; font-size:10px;">（スポンサーリンク）</div>"""
ADS_UNIT_BOTTOM = """<div style="text-align:center; margin:20px 0; color:#ccc; font-size:10px;">（スポンサーリンク）</div>"""

HTML_LAYOUT = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-Brain | エビデンス解析</title>
    {ADSENSE_HEAD_CODE}
    <style>
        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f4f7f6; color: #2c3e50; }}
        .header {{ text-align: center; padding: 40px 20px; background: #fff; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 30px; }}
        h1 {{ margin: 0; font-size: 2.5em; color: #2c3e50; }}
        .search-box {{ text-align: center; margin: 30px 0; }}
        .search-input {{ width: 75%; padding: 18px 25px; border: 2px solid #eee; border-radius: 40px; font-size: 18px; outline: none; transition: 0.3s; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }}
        .search-input:focus {{ border-color: #3498db; box-shadow: 0 4px 20px rgba(52,152,219,0.15); }}
        .article-card {{ background: #fff; padding: 25px; border-radius: 12px; margin-bottom: 20px; border-left: 6px solid #3498db; box-shadow: 0 3px 10px rgba(0,0,0,0.05); }}
        .article-title {{ font-size: 1.2em; color: #2c3e50; margin-bottom: 10px; display: block; }}
        .article-text {{ font-size: 0.95em; color: #7f8c8d; line-height: 1.6; }}
        footer {{ text-align: center; margin-top: 60px; padding: 30px; font-size: 13px; color: #95a5a6; border-top: 1px solid #e0e0e0; }}
        footer a {{ color: #3498db; text-decoration: none; margin: 0 10px; }}
        .btn {{ padding: 18px 35px; background: #2c3e50; color: white; border:
