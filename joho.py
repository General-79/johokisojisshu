import streamlit as st

#stleamlit run ファイル名.py で最初の実行

st.title('初めてのstleamlit')
st.write('これから作品を作っていきます。')

text=st.text_input('あなたの名前を教えてください')
st.write('あなたの名前は、'+text+'です。')

condition=st.slider('あなたの今の調子は？' ,0,100,50)#最小値,最大値,スタート位置
st.write('コンディション：',condition)

option=st.selectbox(
    '好きな数字を教えてください',
    list(['１番','２番','３番','４番'])
)
st.write('あなたが選択したのは、'+option+'です。')

import time
st.sidebar.write('プログレスバーの表示')

latest_iteration=st.empty()#空コンテンツと一緒に変数を作成
bar=st.progress(0)#プログレスをつくる　値は０

for i in range(100):
    latest_iteration.text(f'読み込み中{i+1}')
    bar.progress(i+1)
    time.sleep(0.01)

left_column,right_column=st.columns(2)
button=left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラムです')

from PIL import Image #PILをpip install pillowを実施する
img=Image.open('S__87392259_0.jpg')

st.image(img,caption='そうすけ',use_column_width=True)

import pandas as pd
import numpy as np

df=pd.DataFrame(
    np.random.rand(100,2)/[50,50]+[36.64,138.19],
    columns=['lat','lon',]
)

st.map(df)
st.table(df)
