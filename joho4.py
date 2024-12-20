import streamlit as st

st.title('カード作成機')
st.write('あなたのアップロードした写真をもとにカードを作成します。')
st.write('サイドバーから属性を選択してください')

from PIL import Image, ImageDraw, ImageFont
import io

import os

# フォントファイルのパス
# font_path = "fonts/custom_font.ttf"

# # フォントファイルの存在確認
# if os.path.exists(font_path):
#     print("フォントファイルが見つかりました。")
#     font = ImageFont.truetype(font_path, 30)  # フォントサイズ30で読み込み
# else:
#     print(f"フォントファイルが見つかりません: {font_path}")
#     # フォントが見つからない場合はデフォルトフォントを使用
#     font = ImageFont.load_default()

# 背景画像のリスト（6種類の背景画像を設定）
background_images = {
    "火": "s_1.png",
    "水": "s_2.png",
    "草": "s_3.png",
    "電気": "s_4.png",
    "悪": "s_5.png",
    "回復": "s_6.png",
}

def load_image(image_path):
    """画像を読み込む"""
    return Image.open(image_path)

def combine_images_with_text(background, overlay, position=(0, 0), size=(100, 100), texts=None, text_font=None, text_size=30, text_color=(255, 255, 255)):
    """画像を合成し、複数のテキストを追加する"""
    # 画像をリサイズ
    overlay_resized = overlay.resize(size)
    background.paste(overlay_resized, position, overlay_resized.convert("RGBA").split()[3])  # 透明部分を保持
    
    # 複数のテキストを描画
    if texts:
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype(text_font, text_size) if text_font else ImageFont.load_default()
        for text, text_position, text_color in texts:
            draw.text(text_position, text, font=font, fill=text_color)
    
    return background

def main():
    # サイドバーにタイトルを表示
    st.sidebar.title("画像合成アプリ")

    # ① 背景画像を選択
    selected_background = st.sidebar.selectbox("背景画像を選択してください", list(background_images.keys()))

    # 背景画像を読み込み
    background_image_path = background_images[selected_background]
    background_image = load_image(background_image_path)
    
    # ② ユーザーに画像をアップロードさせる
    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # アップロードされた画像を読み込み
        overlay_image = Image.open(uploaded_image)

        # ③ 画像のリサイズと合成位置を指定
        resize_width = st.sidebar.slider("リサイズの幅", min_value=50, max_value=500, value=100)
        resize_height = st.sidebar.slider("リサイズの高さ", min_value=50, max_value=500, value=100)

        # 合成する位置を選択
        x_pos = st.sidebar.slider("X座標", 0, background_image.width - resize_width, 50)
        y_pos = st.sidebar.slider("Y座標", 0, background_image.height - resize_height, 50)
        position = (x_pos, y_pos)

        # ④ 複数のテキスト入力欄
        num_texts = st.sidebar.number_input("テキストの数", min_value=1, max_value=5, value=1)
        texts = []
        for i in range(num_texts):
            text_input = st.sidebar.text_input(f"テキスト{i+1}", key=f"text_{i}")
            text_position_x = st.sidebar.slider(f"テキスト{i+1}のX座標", 0, background_image.width - 100, 50, key=f"x_{i}")
            text_position_y = st.sidebar.slider(f"テキスト{i+1}のY座標", 0, background_image.height - 100, 50, key=f"y_{i}")
            text_color = st.sidebar.color_picker(f"テキスト{i+1}の色", "#FFFFFF", key=f"color_{i}")
            texts.append((text_input, (text_position_x, text_position_y), text_color))

        # ⑤ テキストのサイズの調整
        text_size = st.sidebar.slider("テキストのサイズ", min_value=10, max_value=100, value=30)

        # フォント設定（ここではデフォルトフォント）
        # フォントファイルのパス
        # text_font = "meiryo"

        
        
        # 画像に合成（複数のテキスト付き）
        combined_image = combine_images_with_text(
            background_image.copy(), overlay_image, position=position, 
            size=(resize_width, resize_height), texts=texts, 
             text_size=text_size
        )

        # 合成した画像を表示
        st.image(combined_image, caption="合成された画像", use_column_width=True)

        # ⑦ 合成画像をダウンロードできるボタン
        buffered = io.BytesIO()
        combined_image.save(buffered, format="PNG")
        buffered.seek(0)
        
        st.download_button(
            label="合成画像をダウンロード",
            data=buffered,
            file_name="combined_image_with_text.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()