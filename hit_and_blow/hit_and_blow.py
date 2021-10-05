# coding: UTF-8
"""
    * File name: hit_and_blow.py
    * Description: hit and blowのmainモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

from sys import api_version
from player import Player
import tkinter as tk
import tkinter.ttk as ttk

ROOT = tk.Tk()
ROOT.geometry("800x600")

ROOT.grid_rowconfigure(0, weight=1)
ROOT.grid_columnconfigure(0, weight=1)

# main フレーム
FRAME_MAIN = ttk.Frame(root)
FRAME_MAIN.grid(row=0, column=0, sticky="nsew", pady=20)



def main():

    #ログイン画面のフレーム
    frame_login = ttk.Frame(ROOT)
    frame_login.grid(row= 0, column= 0, sticky= "nsew", pady= 20)

    label_player_name = ttk.Label(frame_login, text="プレイヤー名を入力してください")
    box_player_name = ttk.Entry(frame_login, width = 50)
    label_player_name.pack()
    box_player_name.pack()

    label_room_id = ttk.Label(frame_login, text="部屋番号を入力してください")
    box_room_id = ttk.Entry(frame_login, width = 50)
    label_room_id.pack()
    box_room_id.pack()

    label_mode = ttk.Label(frame_login, text= "モードを選択(auto -> 1/manual -> 1)")
    box_mode = ttk.Entry(frame_login, width= 50)
    label_mode.pack()
    box_mode.pack()

    def start_game():
        game_player = Player(
            room_id= int(box_room_id.get()),
            player_name= box_player_name.get(),
            mode= int(box_mode.get())
        )

        FRAME_MAIN.tkraise()
        game_player.play_game()

    button = ttk.Button(frame_login, text = "GAME START", width= 50, command= start_game)
    button.pack()

    frame_login.tkraise()
    ROOT.mainloop()



if __name__ == "__main__":

    main()
