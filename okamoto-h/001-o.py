# app.py
# 若者向け選挙検索エンジン（Flask API連携・実用版）

from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = "election.db"

# --- DB初期化 ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            tag TEXT,
            url TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- API：記事一覧取得 ---
@app.route('/api/articles')
def api_articles():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT title, content, tag, url FROM articles")
    rows = c.fetchall()
    conn.close()

    articles = []
    for r in rows:
        articles.append({
            "title": r[0],
            "summary": r[1],
            "tags": r[2].split(','),
            "url": r[3]
        })
    return jsonify(articles)

# --- トップページ ---
@app.route('/')
def index():
    return render_template('index.html')

# --- 初期データ（確認後1回のみ） ---
def insert_sample():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # テスト用の記事データ（title, content, tag, url）
    # tag は「カンマ区切り文字列」で保存する点に注意
    samples = [
        (
            "18歳選挙権とは",
            "18歳になると国政選挙や地方選挙で投票ができます。住民票のある自治体で投票し、投票所では本人確認を行います。",
            "18歳選挙権,投票方法,若者向け",
            "https://www.soumu.go.jp"
        ),
        (
            "投票日に行けないときは？",
            "選挙当日に投票所へ行けない場合でも、期日前投票を利用することができます。期日前投票は公示日後から前日まで可能です。",
            "期日前投票,投票方法,選挙制度",
            "https://www.soumu.go.jp/senkyo/senkyo_s/news/sonota/kininaru.html"
        ),
        (
            "比例代表制って何？",
            "比例代表制とは、政党の得票数に応じて議席が配分される選挙制度です。参議院選挙や衆議院選挙で採用されています。",
            "比例代表制,選挙制度,国政",
            "https://www.soumu.go.jp/senkyo/senkyo_s/news/sonota/hirei.html"
        ),
        (
            "投票所での流れ",
            "投票所では受付後に投票用紙を受け取り、記載台で記入して投票箱に入れます。所要時間は数分程度です。",
            "投票所,投票方法,初心者向け",
            "https://www.soumu.go.jp/senkyo/senkyo_s/news/sonota/nagare.html"
        ),
        (
            "白票って意味あるの？",
            "白票は有効票にはなりませんが、投票率には反映されます。意思表示の一形態として捉えられることもあります。",
            "白票,投票,政治参加",
            "https://www.soumu.go.jp/senkyo/senkyo_s/news/sonota/hakuhyo.html"
        )
    ]

    # 複数件をまとめて INSERT
    c.executemany('''
        INSERT INTO articles (title, content, tag, url)
        VALUES (?, ?, ?, ?)
    ''', samples)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    # insert_sample()  # 初回のみ実行(実行済み)
if __name__ == "__main__":
    init_db()
    # insert_sample()  # 初回のみ実行（※普段はコメントアウト）
    app.run(host="0.0.0.0", port=5000, debug=False)


# --- templates/index.html ---
"""
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>若者のための選挙検索</title>
</head>
<body>
  <h1>若者のための選挙検索</h1>
  <input type="text" id="searchBox" placeholder="例：投票方法" />
  <div id="results"></div>

  <p style="font-size:12px;">※AI要約を人が確認しています。正確な情報は元記事をご確認ください。</p>

  <script>
    let articles = [];

    fetch('/api/articles')
      .then(res => res.json())
      .then(data => {
        articles = data;
        render(articles);
      });

    const searchBox = document.getElementById('searchBox');
    const results = document.getElementById('results');

    function render(list) {
      results.innerHTML = '';
      list.forEach(a => {
        const div = document.createElement('div');
        div.innerHTML = `<h3>${a.title}</h3><p>${a.summary}</p><a href="${a.url}" target="_blank">元記事</a><hr>`;
        results.appendChild(div);
      });
    }

    searchBox.addEventListener('input', () => {
      const k = searchBox.value;
      const filtered = articles.filter(a =>
        a.title.includes(k) ||
        a.summary.includes(k) ||
        a.tags.some(t => t.includes(k))
      );
      render(filtered);
    });
  </script>
</body>
</html>
"""