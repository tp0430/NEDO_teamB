# coding: UTF-8
"""
    * File name: display.py
    * Description: streamlitを使ったGUI用のモジュール
    * Created on: October 3rd
    * Created by: ArowanaArowana
"""

import streamlit as st


def input_screen():
    #タイトル
    st.title("Hit and Blow")
    #プレイヤーネーム入力
    input_text = st.text_input("Please enter your player name", "player name")
    #if文の中身は選択した分岐が問題なく繋がるようにあとで組み替える．以下同様

    #ルームID
    input_text = st.text_input("Please enter the room id", "player name")
    #正当な値を入力するまで入力を促し続ける仕組みなど

    selected_item = st.radio('Please enter the player type.', ['manual', 'auto'])
    #if文の中身は選択した分岐が問題なく繋がるようにあとで組み替える．以下同様
    if selected_item == 'manual':
        pass
    else:
        pass