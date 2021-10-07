# coding: UTF-8
"""
    * File name: display.py
    * Description: streamlitを使ったGUI用のモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import N
from player import Player

class Game:
    player: Player = None
    root: tk.Tk = tk.Tk()

    @classmethod
    def init(cls) -> None:
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
        self.frame.grid(row= 0, column= 0, sticky= "nsew", pady= 20)
    
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
    
    def onclick(self):
        """ログイン画面でボタンを押された時の処理
        playerオブジェクトを作り、入室後、自身の数字登録画面に移行
        :param なし
        :return: なし
        """
        Game.set_player(
            room_id= int(self.box_room_id.get()),
            player_name= self.box_player_name.get(),
            mode= int(self.box_mode.get())
            )
        Game.player._api_com.enter_room()
        Game.show_waiting_disp()

class DispRegisterNum(Disp):

    def __init__(self) -> None:
        super().__init__()

        label = ttk.Label(self.frame, text= "あなたの番号を入力してください")
        self.box_your_num = ttk.Entry(self.frame, width = 50)
        label.pack()
        self.box_your_num.pack()

        button_enter = ttk.Button(self.frame, text= "ENTER", command= self.onclick)
        button_enter.pack()
    
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


class DispPlayingManual(Disp):

    def __init__(self) -> None:

        super().__init__()

        label = ttk.Label(self.frame, text= "相手の数字はなんだと思う？")
        self.box_guess_num = ttk.Entry(self.frame, width= 50)

        label.pack()
        self.box_guess_num.pack()

        self.button = ttk.Button(self.frame, text= "ENTER", command= self.onclick, state= "disable")
        self.button.pack()

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
            guess_result = Game.player.post_guess_num(guess_num= guess_num)

            label_new_guess = tk.Label(self.frame, text= "{} : {}".format(guess_num, guess_result))
            label_new_guess.pack()
        else:
            print("ERROR : unexpected number")
        
        self.box_guess_num.delete(0, tk.END)

    def is_correct_num(self):
        """入力された数字を取得し、それが16進5桁の数字かどうか判定
        :param なし
        :rtype: bool
        :return: 16進5桁の数字ならTrue, そうでなければFalse
        """
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

class DispPlayingAuto(Disp):

    def __init__(self) -> None:
        super().__init__()

        label = tk.Label(self.frame, text= "棋神降臨")
        label.pack()

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
