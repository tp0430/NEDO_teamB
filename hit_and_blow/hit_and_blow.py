# coding: UTF-8
"""
    * File name: hit_and_blow.py
    * Description: hit and blowのmainモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

from player import ManualPlayer, AutoPlayer


def main():
    player_name = input("enter player name: ")
    room_id = int(input("enter room ID: "))
    player_type = input("enter player type (manual/auto): ")
    if player_type == "manual":
        game_player = ManualPlayer(room_id=room_id, player_name=player_name)
    elif player_type == "auto":
        game_player = AutoPlayer(room_id=room_id, player_name=player_name)
    game_player.play_game()


if __name__ == "__main__":
    main()
