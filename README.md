# 週間献立アプリ（PWA）

家族で共有できる週間献立アプリ。Anthropic Claude API（Tool use + Prompt caching）で献立を自動生成し、Firebase Firestore で家族間共有、GitHub Pages でホスティング。

- 📅 週単位の献立カード表示
- ✨ AI（Gemini）で1週間分を一括生成、1日だけ再生成も可能
- 🛒 買い物リストを家族でリアルタイム共有（チェックボックス同期）
- ⭐ お気に入りレシピ保存、次回生成時に優先候補に
- 👨‍👩‍👧‍👦 家族プロフィール（メンバー・除外食材・好み）
- 📚 過去の献立履歴
- 📱 スマホのホーム画面に追加できる PWA

## セットアップ手順

### 1. Firebase プロジェクトを作成

1. https://console.firebase.google.com/ にアクセス
2. 「プロジェクトを作成」→ 名前は何でも OK（例: `kondate-app`）
3. Google Analytics は **オフ** で OK
4. 作成後、左メニューから **Authentication** → 「始める」→ **Sign-in method** タブ → **匿名（Anonymous）** を有効化
5. 左メニューから **Firestore Database** → 「データベースを作成」→ ロケーション asia-northeast1 → 本番モードで開始
6. プロジェクト設定（左上の歯車アイコン）→ 「マイアプリ」で **Web アプリ（</> アイコン）** を追加
7. 表示された `firebaseConfig` を控える

### 2. index.html に Firebase 設定を貼り付け

`index.html` の冒頭にある以下の部分を、上で控えた値で書き換える:

```js
const firebaseConfig = {
  apiKey: "YOUR_API_KEY_HERE",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.firebasestorage.app",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

### 3. Firestore セキュリティルールを適用

`firestore.rules` の内容を、Firebase Console の **Firestore Database** → **ルール** タブに貼り付け → 公開。

または Firebase CLI を使う場合:
```bash
npm install -g firebase-tools
firebase login
firebase use --add  # プロジェクトを選択
firebase deploy --only firestore:rules
```

### 4. GitHub Pages で公開

1. このリポジトリの **Settings** → **Pages**
2. **Source** = `Deploy from a branch`
3. **Branch** = `main` / `/ (root)` → Save
4. 数十秒後に `https://l91005025-png.github.io/kondate-app/` で公開される

### 5. 家族で使い始める

1. 公開された URL にスマホでアクセス
2. ホーム画面に追加（Safari: 共有 → ホーム画面に追加 / Chrome: メニュー → アプリをインストール）
3. **家族コード**（任意の合言葉、例: `tanaka-2026`）と自分の名前を入力
4. 設定タブで **Anthropic API キー** を登録（[Anthropic Console](https://console.anthropic.com/settings/keys) で作成。Pro プランとは別に最低5ドルのクレジット購入が必要）
5. 家族メンバーには **同じ家族コード** を共有してもらう

## データ構造（Firestore）

```
families/
  {familyId}/                       # 家族コード
    members: [{ uid, name }, ...]
    profile/main                    # プロフィール（メンバー・除外食材）
    menus/{YYYY-MM-DD}/             # 週の月曜日をキーにした献立
      weekStart, days[], shoppingList, shoppingChecked
    favorites/{recipeId}/           # お気に入りレシピ
```

## 注意事項

- **Anthropic API キーは各端末のブラウザに保存される**（共有はされない）。各人が自分のキーを取得して登録。
- デフォルトモデルは **Claude Haiku 4.5**（家族用途で月数十円〜）。設定で Sonnet 4.5 にも切替可能。
- 家族コードは「共有秘密」として機能。**他人に知られると献立データが見える**ので、推測しにくいものを選ぶ。
- Firebase の無料枠（Spark プラン）で十分動作する想定。

## 旧アプリ（Streamlit版）について

このリポジトリは Streamlit 版から PWA に作り直したものです。旧コード（`app.py`、`requirements.txt`）は削除しました。
