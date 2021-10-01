# coding: UTF-8
"""
    * File name: hit_and_blow.py
    * Description: hit and blowのmainモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

import requests
import time
import pprint

from communication import APICom

room_id = 2125
player_name = "B"
player_id = "7d025351-7836-4904-a48f-f58019b6ca77"
hidden_num = "abcde"

def input_init_info():

    room_id = int(input("enter room id --- "))
    player_name = input("enter player name --- ")
    player_id = input("enter player id --- ")

    hidden_num = input("enter hidden number --- ")

if __name__ == "__main__":

    api_com = APICom(player_id=player_id, player_name=player_name, room_id=room_id)
    result_enter_room = api_com.enter_room()

    pprint(result_enter_room)

    while api_com.get_room()["state"] == 1:
        time.sleep(1)
    
    while api_com.get_room()["state"] == 2:

        if api_com.get_table()["now_player"] == api_com._player_name:
            guess_num = input("enter guess number --- ")

            api_com.post_guess(guess_number = guess_num)
        
        time.sleep(1)
    
    if api_com.get_table()["winner"] == api_com._player_name:

        print("YOU WIN !!")
    else:
        print("YOU LOSE")

