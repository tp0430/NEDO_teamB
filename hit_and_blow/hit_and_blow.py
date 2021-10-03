# coding: UTF-8
"""
    * File name: hit_and_blow.py
    * Description: hit and blowのmainモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

from player import Player


def main():
    player_name = input("enter player name: ")
    room_id = int(input("enter room ID: "))
    player_type = input("enter player type (manual/auto): ")
    if player_type == "manual":
        game_player = Player(room_id=room_id, player_name=player_name)
    elif player_type == "auto":
        game_player = Player(room_id=room_id, player_name=player_name, mode= 1)
    game_player.play_game()


if __name__ == "__main__":
    main()
