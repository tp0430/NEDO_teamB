# coding: UTF-8
"""
    * File name: hit_and_blow.py
    * Description: hit and blowのmainモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""
import streamlit as st

from player import Player


def main():
    st.title("Hit and Blow")
    player_name = st.text_input("PLAYER NAME")
    room_id = int(st.text_input("ROOM ID"))
    player_type = st.text_input("PLAYER TYPE (manual/auto)")
    if player_type == "manual":
        game_player = Player(room_id=room_id, player_name=player_name)
    elif player_type == "auto":
        game_player = Player(room_id=room_id, player_name=player_name, mode= 1)
    game_player.play_game()


if __name__ == "__main__":
    main()
