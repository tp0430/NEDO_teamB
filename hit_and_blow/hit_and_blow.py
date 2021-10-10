# coding: UTF-8
"""
    * File name: hit_and_blow.py
    * Description: hit and blowのmainモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""
import streamlit as st

from player import Player

import json
import os


def main():
    """
    print(os.getcwd())
    json_path = os.path.join("save_file","register.json")
    json_open = open(json_path, "r+")
    json_load = json.load(json_open)
    print(json_load["game_count"]["game_num"] )
    json_open.close()
    """

    st.title("Hit and Blow")
    player_name = st.text_input("PLAYER NAME")
    room_id = int(st.number_input("ROOM ID"))
    player_mode = st.radio("Select game mode", ["manual", "auto"])
    if len(player_name) != 0 and room_id != 0:
        if player_mode == "manual":
            game_player = Player(room_id=room_id, player_name=player_name)
        elif player_mode == "auto":
            game_player = Player(room_id=room_id, player_name=player_name, mode=1)
        game_player.play_game()
        json_path = os.path.join("save_file", "register.json")
        json_open = open(json_path, "r+")
        json_load = json.load(json_open)
        json_load["game_count"]["game_num"] += 1
        json_open.close()


if __name__ == "__main__":
    main()
