# coding: UTF-8
"""
    * File name: display.py
    * Description: streamlitを使ったGUI用のモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

import tkinter as tk
import tkinter.ttk as ttk


def main():
    # rootウィンドウ
    root = tk.Tk()
    root.title("test_login_screen")
    root.geometry("800x600")

    # よくわからないが、グリッドを1x1にしている(らしい)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    #ログイン画面のフレーム
    frame_login = ttk.Frame(root)
    frame_login.grid(row= 0, column= 0, sticky= "nsew", pady= 20)

    label_player_name = ttk.Label(frame_login, text="プレイヤー名を入力してください")
    box_player_name = ttk.Entry(frame_login, width = 50)
    label_player_name.pack()
    box_player_name.pack()

    label_room_id = ttk.Label(frame_login, text="部屋番号を入力してください")
    box_room_id = ttk.Entry(frame_login, width = 50)
    label_room_id.pack()
    box_room_id.pack()

    # main フレーム
    frame_main = ttk.Frame(root)
    frame_main.grid(row=0, column=0, sticky="nsew", pady=20)
    label_main = ttk.Label(frame_main, text= "メインフレーム")
    label_main.pack()

    def myclick():
        print("player name: {}".format(box_player_name.get()))
        print("room id: {}".format(box_room_id.get()))
        button["state"] = tk.DISABLED
        frame_main.tkraise()

    button = ttk.Button(frame_login, text = "Enter", width= 50, command= myclick)
    button.pack()

    frame_login.tkraise()

    root.mainloop()


if __name__ == "__main__":
    main()