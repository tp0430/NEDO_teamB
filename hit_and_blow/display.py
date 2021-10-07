# coding: UTF-8
"""
    * File name: display.py
    * Description: streamlitを使ったGUI用のモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

import tkinter as tk
from tkinter.constants import N
import tkinter.ttk as ttk

from player import Player



class Game:
    player: Player = None
    root: tk.Tk = tk.Tk()

    @classmethod
    def init(cls) -> None:
        Game.root.geometry("800x600")
        Game.root.grid_rowconfigure(0, weight=1)
        Game.root.grid_columnconfigure(0, weight=1)
    
    @classmethod
    def set_player(cls, room_id: int, player_name: str, mode: int):
        Game.player = Player(room_id= room_id, player_name= player_name, mode= mode)

        print("player info: room id:{}, name:{}, mode{}".format(room_id, player_name, mode))
    
    @classmethod
    def show_login_disp(cls):
        disp = DispLogin()
        disp.show()

    @classmethod
    def show_waiting_disp(cls):
        disp = DispWaiting()
        disp.show()

    @classmethod
    def show_playing_manual_disp(cls):
        disp = DispPlayingManual()
        disp.show()

    @classmethod
    def show_playing_auto_disp(cls):
        disp = DispPlayingAuto()
        disp.show()

    @classmethod
    def show_reslut_disp(cls):
        disp = DispResult()
        disp.show()

class DispLogin:

    def __init__(self) -> None:
        self.frame = ttk.Frame(Game.root)
        self.frame.grid(row= 0, column= 0, sticky= "nsew", pady= 20)

        label_player_name = ttk.Label(self.frame, text="プレイヤー名を入力してください")
        self.box_player_name = ttk.Entry(self.frame, width = 50)
        label_player_name.pack()
        self.box_player_name.pack()

        label_room_id = ttk.Label(self.frame, text="部屋番号を入力してください")
        self.box_room_id = ttk.Entry(self.frame, width = 50)
        label_room_id.pack()
        self.box_room_id.pack()

        label_mode = ttk.Label(self.frame, text= "モードを選択(auto: 1 / manual: 0)")
        self.box_mode = ttk.Entry(self.frame, width= 50)
        label_mode.pack()
        self.box_mode.pack()

        self.button_login = ttk.Button(self.frame, text = "GAME START", command= self.onclick)
        self.button_login.pack()
    
    def show(self):
        print("disp login")
        self.frame.tkraise()
    
    def onclick(self):
        Game.set_player(
            room_id= int(self.box_room_id.get()),
            player_name= self.box_player_name.get(),
            mode= int(self.box_mode.get())
            )
        Game.player._api_com.enter_room()
        Game.show_waiting_disp()

class DispWaiting:

    def __init__(self) -> None:
        self.frame = ttk.Frame(Game.root)
        self.frame.grid(row= 0, column= 0, sticky= "nsew", pady= 20)

        label = ttk.Label(self.frame, text= "あなたの番号を入力してください")
        self.box_your_num = ttk.Entry(self.frame, width = 50)
        label.pack()
        self.box_your_num.pack()

        button_enter = ttk.Button(self.frame, text= "ENTER", command= self.onclick)
        button_enter.pack()
    
    def onclick(self):
        print("clicked in disp_waiting")
        if self.is_correct_num():
            print("correct number")
            print("my number : {}, type : {}".format(self.box_your_num.get(), type(self.box_your_num.get())))
            Game.player._api_com.post_hidden(self.box_your_num.get())

            if Game.player.mode:
                Game.show_playing_auto_disp()
            else:
                Game.show_playing_manual_disp()

    
    def is_correct_num(self):
        num = self.box_your_num.get()
        if len(num) != 5:
            return False
        for element in num:
            try:
                int(element, 16)
                pass
            except ValueError:
                return False
        return True

    def show(self):
        self.frame.tkraise()

class DispPlayingManual:

    def __init__(self) -> None:

        self.frame = ttk.Frame(Game.root)
        self.frame.grid(row= 0, column= 0, sticky= "nsew", pady= 20)

        label = ttk.Label(self.frame, text= "相手の数字はなんだと思う？")
        self.box_guess_num = ttk.Entry(self.frame, width= 50)
        label.pack()
        self.box_guess_num.pack()

        self.button = ttk.Button(self.frame, text= "ENTER", command= self.onclick, state= "disable")
        self.button.pack()
        self.frame.after(1000, self.update_game_state)
    
    def update_game_state(self):

        game_state = Game.player.get_game_state()
        if game_state == 2:
            if Game.player.is_my_turn():
                self.button["state"] = tk.NORMAL
            else:
                self.button["state"] = tk.DISABLED
        elif game_state == 3:
            Game.show_reslut_disp()


        self.frame.after(1000, self.update_game_state)
    
    
    def onclick(self):

        if self.is_correct_num():
            guess_num = self.box_guess_num.get()
            guess_result = Game.player.post_guess_num(guess_num= guess_num)

            label_new_guess = tk.Label(self.frame, text= "{} : {}".format(guess_num, guess_result))
            label_new_guess.pack()
        else:
            print("ERROR : unexpected number")
        
        self.box_guess_num.delete(0, tk.END)

    def is_correct_num(self):
        num = self.box_guess_num.get()
        if len(num) != 5:
            return False
        for element in num:
            try:
                int(element, 16)
                pass
            except ValueError:
                return False
        
        return True

    def show(self):
        self.frame.tkraise()

class DispPlayingAuto:

    def __init__(self) -> None:
        self.frame = tk.Frame(Game.root)
        self.frame.grid(row= 0, column= 0, sticky= "nsew", pady= 20)

        label = tk.Label(self.frame, text= "棋神降臨")
        label.pack()

        self.frame.after(1000, self.update_game_state)

    def update_game_state(self):

        game_state = Game.player.get_game_state()

        if game_state == 2 and Game.player.is_my_turn():
            guess_num = Game.player.auto_guess()
            guess_result = Game.player.post_guess_num(guess_num)

            label_new_guess = tk.Label(self.frame, text= "{} : {}".format(guess_num, guess_result))
            label_new_guess.pack()

        elif game_state == 3:
            Game.show_reslut_disp()
        
        self.frame.after(1000, self.update_game_state)
    
    def show(self):
        self.frame.tkraise()

class DispResult:

    def __init__(self) -> None:
        self.frame = tk.Frame(Game.root)
        self.frame.grid(row= 0, column= 0, sticky= "nsew", pady= 20)

        label : tk.Label
        winner = Game.player.get_winner()
        if winner == Game.player._player_name:
            label = tk.Label(self.frame, text= "WIN!")
        elif winner == None:
            label = tk.Label(self.frame, text= "DRAW")
        else:
            label = tk.Label(self.frame, text= "ROSE")
        label.pack()
    
    def show(self):
        self.frame.tkraise()



if __name__ == "__main__":
    pass