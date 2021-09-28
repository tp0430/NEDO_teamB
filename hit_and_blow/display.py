# coding: UTF-8
"""
    * File name: display.py
    * Description: streamlitを使ったGUI用のモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

import streamlit as st


def display_test():
    # Streamlit が対応している任意のオブジェクトを可視化する (ここでは文字列)
    # タイトル
    st.title('Application title')
    # ヘッダ
    st.header('Header')
    #テキストを入力
    input_text = st.text_input("何か入力してみて", "something")
    #入力されたテキストを出力
    st.text("入力された文字は:")

    if input_text == "amongus":
        st.header("AMONGUS")
    else:
        st.text(input_text)

    # サブレベルヘッダ
    st.subheader('Sub header')
    # マークダウンテキスト
    st.markdown('**Markdown is available **')
    # LaTeX テキスト
    st.latex(r'\bar{X} = \frac{1}{N} \sum_{n=1}^{N} x_i')
    # コードスニペット
    st.code('print(\'Hello, World!\')')
    # エラーメッセージ
    st.error('Error message')
    # 警告メッセージ
    st.warning('Warning message')
    # 情報メッセージ
    st.info('Information message')
    # 成功メッセージ
    st.success('Success message')
    # 例外の出力
    st.exception(Exception('Oops!'))
    # 辞書の出力
    d = {
        'foo': 'bar',
        'users': [
            'alice',
            'bob',
        ],
    }
    st.json(d)


