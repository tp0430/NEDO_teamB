# coding: UTF-8
"""
    * File name: test_hit_and_blow.py
    * Description: hit_and_blow.pyのmain関数をテストする
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

import requests
import time

from hit_and_blow.communication import APICom

room_id = 0
player_name = ""
player_id = ""
room_id = 0
hidden_num = "abcde"

def input_init_info():

    room_id = int(input("enter room id --- "))
    player_name = input("enter player name --- ")
    player_id = input("enter player id --- ")
    room_id = input("enter room id --- ")

    hidden_num = input("enter hidden number --- ")

if __name__ == "__main__":

    input_init_info()
    api_com = APICom(player_id=player_id, player_name=player_name, room_id=room_id)
    api_com.enter_room()

    while api_com.get_room()["state"] == 1:
        time.sleep(1)
    
    while api_com.get_room()["state"] == 2:

        if api_com.get_table()["now_player"] == api_com.player_name:
            guess_num = input("enter guess number --- ")

            api_com.post_guess(guess_number = guess_num)
        
        time.sleep(1)
    
    if api_com.get_table()["winner"] == api_com.player_name:

        print("YOU WIN !!")
    else:
        print("YOU LOSE")

