import streamlit as st
import anthropic

st.set_page_config(page_title="週間献立アプリ", page_icon="🍽️", layout="wide")
st.title("🍽️ 週間献立自動作成アプリ")
st.caption("家族4人（父・母・息子6歳・娘3歳）向け")

api_key = st.secrets.get("ANTHROPIC_API_KEY", "") or st.sidebar.text_input("Claude APIキーを入力", type="password")
st.sidebar.markdown("---")
st.sidebar.markdown("### 設定")
exclude_foods = st.sidebar.text_input("除外したい食材（例：セロリ、ピーマン）")
max_time = st.sidebar.selectbox("調理時間の目安", ["指定なし", "30分以内", "45分以内", "1時間以内"])

if st.button("今週の献立を生成する", type="primary", use_container_width=True):
    if not api_key:
        st.error("APIキーを入力してください")
    else:
        with st.spinner("献立を考えています...少々お待ちください"):
            client = anthropic.Anthropic(api_key=api_key)

            exclude_text = f"除外食材: {exclude_foods}" if exclude_foods else ""
            time_text = f"調理時間: {max_time}" if max_time != "指定なし" else ""

            prompt = f"""
家族4人（父30代・母30代・息子6歳・娘3歳）の1週間分（月〜日）の夕食献立を作成してください。

条件:
- 各日: 主菜1品＋副菜1〜2品
- 子どもが食べやすい味付け（辛さ控えめ）
- 栄養バランスよく（肉・魚・野菜をバランスよく）
- 同じ食材を複数日で使い回せるよう工夫する
{exclude_text}
{time_text}

以下の形式で出力してください:

## 月曜日
**主菜**: [料理名]
**副菜**: [料理名]、[料理名]

（火〜日も同様に）

---
## 📝 まとめ買いリスト

### 肉・魚
- [食材名]: [量]

### 野菜
- [食材名]: [量]

### その他
- [食材名]: [量]

---
## 🍳 レシピ集

### 月曜日: [主菜名]
**材料（4人分）**
- [材料]: [量]

**作り方**
1. [手順]
2. [手順]
（以下詳細に）

（全料理のレシピを記載）
"""

            message = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=8096,
                messages=[{"role": "user", "content": prompt}]
            )

            result = message.content[0].text

            tabs = st.tabs(["📅 週間献立", "🛒 買い物リスト", "🍳 レシピ集"])

            sections = result.split("---")

            with tabs[0]:
                if len(sections) > 0:
                    st.markdown(sections[0])

            with tabs[1]:
                if len(sections) > 1:
                    st.markdown(sections[1])

            with tabs[2]:
                if len(sections) > 2:
                    st.markdown(sections[2])
