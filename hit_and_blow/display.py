# coding: UTF-8
"""
    * File name: display.py
    * Description: streamlitを使ったGUI用のモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import N, X, Y
from player import Player
from typing import List
from PIL import Image, ImageTk

class Game:
    player: Player = None
    root: tk.Tk

    @classmethod
    def init(cls) -> None:
        Game.root = tk.Tk()
        Game.root.geometry("800x600")
        Game.root.grid_rowconfigure(0, weight=1)
        Game.root.grid_columnconfigure(0, weight=1)

        Game.show_login_disp()

    
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
        disp = DispRegisterNum()
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

class Disp:
    """表示フレームを作るクラス、そのままでは何もない画面なので継承して使う
    :param frame ttk.Frame: 表示フレーム
    :func show(): フレームを最前面に持ってくる
    """
    def __init__(self) -> None:
        self.frame = ttk.Frame(Game.root)
        self.frame.grid(row=0, column=0, sticky="nsew", pady=0)
        self.bg_image: tk.PhotoImage
        self.play_image = tk.PhotoImage(file=r"img\button\PLAY.png")
        self.start_image = tk.PhotoImage(file= os.path.join("img", "button", "START.png"))
        self.send_image = tk.PhotoImage(file= os.path.join("img", "button", "SEND.png"))

    def show(self) -> None:
        """オブジェクトのフレームを最前面に持ってくる
        :param なし
        :return: なし
        """
        self.frame.tkraise()
        return

class DispLogin(Disp):

    def __init__(self) -> None:
        super().__init__()
        self.bg_image = tk.PhotoImage(file= os.path.join("img", "back", "login.png"))
        
        label_bg = tk.Label(
            master=self.frame,
            image=self.bg_image,
            width=800,
            height=600
        )
        label_bg.place(x=0, y=0)

        self.button_login = tk.Button(
            self.frame, 
            highlightbackground="#ffffff", 
            width=166, height=33, 
            image=self.play_image, 
            command=self.onclick)

        self.button_login.place(anchor="c", x=292, y=493)

        label_player_name = ttk.Label(
            self.frame, text="プレイヤー名を入力してください", background="white"
        )
        self.box_player_name = ttk.Entry(self.frame, width=30)
        label_player_name.place(anchor="c", x=292, y=250)
        self.box_player_name.place(anchor="c", x=292, y=280)

        label_room_id = ttk.Label(self.frame, text="部屋番号を入力してください", background="white")
        self.box_room_id = ttk.Entry(self.frame, width=30)
        label_room_id.place(anchor="c", x=292, y=330)
        self.box_room_id.place(anchor="c", x=292, y=360)

        label_mode = ttk.Label(
            self.frame, text="モードを選択(auto: 1 / manual: 0)", background="white"
        )
        self.box_mode = ttk.Entry(self.frame, width=30)
        label_mode.place(anchor="c", x=292, y=410)
        self.box_mode.place(anchor="c", x=292, y=440)

        

    def onclick(self):
        """ログイン画面でボタンを押された時の処理
        playerオブジェクトを作り、入室後、自身の数字登録画面に移行
        :param なし
        :return: なし
        """

        room_id: int
        mode: int
        try:
            room_id = int(self.box_room_id.get())
            mode = int(self.box_mode.get())

            if mode != 0 and mode != 1:
                raise ValueError
        except ValueError:
            self.box_room_id.delete(0, tk.END)
            self.box_mode.delete(0, tk.END)
            return
        
        Game.set_player(
            room_id= room_id,
            player_name=self.box_player_name.get(),
            mode= mode,
        )
        Game.player._api_com.enter_room()
        Game.show_waiting_disp()

class DispRegisterNum(Disp):

    def __init__(self) -> None:
        super().__init__()

        self.bg_image = tk.PhotoImage(file= os.path.join("img", "back", "hidden_input.png"))
        label_bg = tk.Label(
            master=self.frame,
            image=self.bg_image,
            width=800,
            height=600
        )
        label_bg.place(x=0, y=0)

        label = ttk.Label(
            self.frame, 
            text="あなたの番号を入力してください", 
            background="white"
            )
        self.box_your_num = ttk.Entry(self.frame, width=30)
        label.place(anchor= tk.CENTER, x= 400, y= 280)
        self.box_your_num.place(anchor= tk.CENTER, x= 400, y= 300)

        button_enter = tk.Button(
            self.frame, 
            highlightbackground="#ffffff", 
            width=166, height=33, 
            image= self.start_image, 
            command=self.onclick)
        button_enter.place(anchor= "c", x= 400, y= 355)

    def onclick(self):
        """自身の数字登録画面でEnterが押された時の処理
        入力されている数字が正しければ、サーバに登録し、モードに応じた画面に移行
        そうでなければ入力ボックスを空にする
        :param なし
        :return: なし
        """
        if self.is_correct_num():
            Game.player._api_com.post_hidden(self.box_your_num.get())

            if Game.player.mode:
                Game.show_playing_auto_disp()
            else:
                Game.show_playing_manual_disp()
        else:
            self.box_your_num.delete(0, tk.END)

    def is_correct_num(self):
        """入力された数字を取得し、それが16進5桁の数字かどうか判定
        :param なし
        :rtype: bool
        :return: 16進5桁の数字ならTrue, そうでなければFalse
        """
        box = set()
        num = self.box_your_num.get()
        if len(num) != 5:
            return False
        for digit in num:
            try:
                if int(digit, 16) in box:
                    return False
                box.add(int(digit, 16))
            except ValueError:
                return False
        return True


class DispPlayingManual(Disp):

    def __init__(self) -> None:

        super().__init__()
        self.bg_image = tk.PhotoImage(file= os.path.join("img", "back", "match.png"))
        label_bg = tk.Label(
            master=self.frame,
            image=self.bg_image,
            width=800,
            height=600
        )
        label_bg.place(x=0, y=0)

        self.box_guess_num = ttk.Entry(
            self.frame, 
            font= ("", 20),
            foreground= "#3fe000",
            width=10, 
            justify= tk.CENTER)

        self.box_guess_num.place(x= 250, y= 535)

        self.button = tk.Button(
            self.frame, 
            highlightbackground="#ffffff", 
            width=150, height=33, 
            image= self.send_image, 
            command=self.onclick, 
            state= tk.NORMAL)
        self.button.place(x= 577, y= 531)

        self.canvas_you_guess = tk.Canvas(
            self.frame, 
            width= 120,
            height= 300, 
            borderwidth= 0, 
            bg= "#3fe000"
        )
        self.canvas_you_guess.place(anchor= tk.CENTER, x= 162, y= 335)
        self.canvas_you_response = tk.Canvas(
            self.frame, 
            width= 120,
            height= 300, 
            borderwidth= 0, 
            bg= "#3fe000"
        )
        self.canvas_you_response.place(anchor= tk.CENTER, x= 300, y= 335)

        self.y_interval = 20
        self.y_you_guess = 13
        self.y_you_responce = 13

        self.img_response = ImageTk.PhotoImage(
            Image.open(os.path.join("img", "response", "sample_response.png"))
            )
        # check_interval ms 事にゲームの状態を確認
        self.check_interval = 1000
        self.frame.after(self.check_interval, self.update_game_state)
    
    def update_game_state(self):
        """ゲームの状態を更新
        ゲーム進行中で自身のターンなら、Enterボタンを有効にする。
        ゲーム進行で自分のターンでなければEnterボタンを無効にする。
        ゲームが終了していたら、結果表示画面に移行
        :param なし
        :rtype: bool
        :return: 16進5桁の数字ならTrue, そうでなければFalse
        """
        game_state = Game.player.get_state()
        if game_state == 2:
            if Game.player.is_my_turn():
                self.button["state"] = tk.NORMAL
            else:
                self.button["state"] = tk.DISABLED
        elif game_state == 3:
            Game.show_reslut_disp()


        self.frame.after(1000, self.update_game_state)
    
    
    def onclick(self):
        """マニュアルモードで進行中の画面でEnterボタンが押された時の処理
        入力されている数字が正常なら、サーバに登録
        :param なし
        :return: なし
        """
        if self.is_correct_num():
            guess_num = self.box_guess_num.get()
            self.canvas_you_guess.create_text(
                60, 
                self.y_you_guess, 
                text= guess_num, 
                fill= "#ffffff", 
                font= ("", 15, "bold")
                )
            self.y_you_guess += self.y_interval

            guess_result = Game.player.post_guess_num(guess_num= guess_num)
            self.canvas_you_response.create_image(
                60,
                self.y_you_responce,
                image= self.img_response
            )
            self.y_you_responce += self.y_interval


        else:
            print("ERROR : unexpected number")
        
        self.box_guess_num.delete(0, tk.END)

    def is_correct_num(self):
        """入力された数字を取得し、それが16進5桁の数字かどうか判定
        :param なし
        :rtype: bool
        :return: 16進5桁の数字ならTrue, そうでなければFalse
        """
        box = set()
        num = self.box_guess_num.get()
        if len(num) != 5:
            return False
        for digit in num:
            try:
                if int(digit, 16) in box:
                    return False
                box.add(digit)
            except ValueError:
                return False
        
        return True


class DispPlayingAuto(Disp):
    def __init__(self) -> None:
        super().__init__()
        self.bg_image = tk.PhotoImage(file= os.path.join("img", "back", "match.png"))
        label_bg = tk.Label(
            master=self.frame,
            image=self.bg_image,
            width=800,
            height=600
        )
        label_bg.place(x=0, y=0)        

        # check_interval ms 事にゲームの状態を確認
        self.check_interval = 1000
        self.frame.after(self.check_interval, self.update_game_state)

    def update_game_state(self):
        """ゲームの状態の更新及び更新時の処理
        ゲームが進行中で、自分のターンなら自動推測してサーバに登録
        ゲームが終了していたら結果画面を表示
        :param なし
        :return: なし
        """
        game_state = Game.player.get_state()
        if game_state == 2 and Game.player.is_my_turn():
            guess_num = Game.player.auto_guess()
            guess_result = Game.player.post_guess_num(guess_num)

            label_new_guess = tk.Label(self.frame, text= "{} : {}".format(guess_num, guess_result))
            label_new_guess.pack()

        elif game_state == 3:
            Game.show_reslut_disp()
        
        self.frame.after(self.check_interval, self.update_game_state)


class DispResult(Disp):

    def __init__(self) -> None:
        super().__init__()

        label : tk.Label
        winner = Game.player.get_winner()
        if winner == Game.player._player_name:
            label = tk.Label(self.frame, text= "WIN!")
        elif winner == None:
            label = tk.Label(self.frame, text= "DRAW")
        else:
            label = tk.Label(self.frame, text= "ROSE")
        label.pack()

def disp_test():
    root = tk.Tk()
    root.geometry("800x600")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frame = tk.Frame(root, bg="#555")
    frame.grid(row= 0, column= 0, sticky= "nsew")

    button_image = tk.PhotoImage(file= "img\kaji_kasaihouchiki_button.png").subsample(4, 4)
    buttons: List[tk.Button] = [None] * 16
    for i in range(16):
        buttons[i] = tk.Button(
            frame,
            width= 80,
            height= 80,
            image= button_image,
            text= "b{}".format(hex(i)[2:]))
        
        buttons[i].place(x= int(i % 4) * 90 + 430, y= int(i / 4) * 90 + 200)
    
    

    root.mainloop()

if __name__ == "__main__":

    disp_test()