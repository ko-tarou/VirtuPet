// server.js
const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const bodyParser = require("body-parser");

const app = express();
const port = 5000;

const cors = require("cors");
app.use(cors());

// データベースの接続
let db = new sqlite3.Database("./data.db", (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log("Connected to the database.");
});

// テーブル作成（初回のみ）
db.serialize(() => {
  // ユーザーテーブル
  db.run(
    `CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT NOT NULL
    )`
  );

  // 動物の設定を保存するテーブル
  db.run(
    `CREATE TABLE IF NOT EXISTS animals (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      type TEXT NOT NULL,
      size TEXT NOT NULL,
      userId INTEGER,
      FOREIGN KEY (userId) REFERENCES users(id)
    )`
  );

  // 背景設定を保存するテーブル
  db.run(
    `CREATE TABLE IF NOT EXISTS backgrounds (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      url TEXT NOT NULL,
      isActive INTEGER DEFAULT 0
    )`
  );
});

// JSONのパーサー
app.use(bodyParser.json());

// ユーザー情報を追加するエンドポイント
app.post("/api/users", (req, res) => {
  const { name, email } = req.body;
  db.run(
    `INSERT INTO users (name, email) VALUES (?, ?)`,
    [name, email],
    function (err) {
      if (err) {
        console.error(err.message);
        res.status(500).send("データの保存に失敗しました。");
      } else {
        res.status(201).send(`ユーザーが追加されました。ID: ${this.lastID}`);
      }
    }
  );
});

// 動物情報を追加するエンドポイント
app.post("/api/animals", (req, res) => {
  const { type, size, userId } = req.body;
  db.run(
    `INSERT INTO animals (type, size, userId) VALUES (?, ?, ?)`,
    [type, size, userId],
    function (err) {
      if (err) {
        console.error(err.message);
        res.status(500).send("動物データの保存に失敗しました。");
      } else {
        res.status(201).send(`動物が追加されました。ID: ${this.lastID}`);
      }
    }
  );
});

// 背景情報を取得するエンドポイント
app.get("/api/backgrounds", (req, res) => {
  db.all(`SELECT * FROM backgrounds WHERE isActive = 1`, [], (err, rows) => {
    if (err) {
      res.status(500).send("背景データの取得に失敗しました。");
    } else {
      res.status(200).json(rows);
    }
  });
});

// 背景を草原に変更するエンドポイント
app.post("/api/backgrounds/set-grassland", (req, res) => {
  db.run(
    `UPDATE backgrounds SET isActive = 0; UPDATE backgrounds SET isActive = 1 WHERE name = 'grassland'`,
    function (err) {
      if (err) {
        console.error(err.message);
        res.status(500).send("背景の設定に失敗しました。");
      } else {
        res.status(200).send("背景が草原に変更されました。");
      }
    }
  );
});

// すべてのユーザー情報を取得するエンドポイント
app.get("/api/users", (req, res) => {
  db.all(`SELECT * FROM users`, [], (err, rows) => {
    if (err) {
      res.status(500).send("データの取得に失敗しました。");
    } else {
      res.status(200).json(rows);
    }
  });
});

// サーバーを起動
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
