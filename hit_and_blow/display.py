# coding: UTF-8
"""
    * File name: display.py
    * Description: streamlitを使ったGUI用のモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""
import os
import glob

import tkinter as tk
from tkinter import font
import tkinter
import tkinter.ttk as ttk
from tkinter.constants import N, NO, X, Y
from player import Player
from typing import List
from PIL import Image, ImageTk

from player import get_save

CHOICES = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
        ]

class Game:
    player: Player = None
    root: tk.Tk

    @classmethod
    def init(cls) -> None:
        Game.player = None
        Game.root = tk.Tk()
        Game.root.geometry("800x600")
        Game.root.grid_rowconfigure(0, weight=1)
        Game.root.grid_columnconfigure(0, weight=1)
        Game.font_jpn = font.Font(Game.root, family="游ゴシック", size=10)
        Game.font_jpn_bold = font.Font(
            Game.root, family="游ゴシック", size=10, weight="bold"
        )
        Game.font_jpn_large = font.Font(
            Game.root, family="游ゴシック", size=13, weight="bold"
        )
        Game.font_eng = font.Font(
            Game.root, family="YU Gothic UI", size=15, weight="bold"
        )
        Game.font_eng_num = font.Font(
            Game.root, family="YU Gothic UI", size=13, weight="bold"
        )

        Game.show_login_disp()

    @classmethod
    def set_player(cls, room_id: int, player_name: str, mode: int):
        Game.player = Player(room_id=room_id, player_name=player_name, mode=mode)

        print(
            "player info: room id:{}, name:{}, mode{}".format(
                room_id, player_name, mode
            )
        )

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
        self.start_image = tk.PhotoImage(
            file=os.path.join("img", "button", "START.png")
        )
        self.send_image = tk.PhotoImage(file=os.path.join("img", "button", "SEND.png"))

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
        self.bg_image = tk.PhotoImage(file=os.path.join("img", "back", "login.png"))

        label_bg = tk.Label(
            master=self.frame, image=self.bg_image, width=800, height=600
        )
        label_bg.place(x=0, y=0)

        self.button_login = tk.Button(
            self.frame,
            highlightbackground="#ffffff",
            width=166,
            height=33,
            image=self.play_image,
            command=self.onclick,
        )

        self.button_login.place(anchor="c", x=292, y=493)

        label_player_name = ttk.Label(
            self.frame,
            text="プレイヤー名を入力",
            foreground="#333f50",
            background="white",
            font=Game.font_jpn_bold,
        )
        self.box_player_name = ttk.Entry(self.frame, width=30)
        label_player_name.place(anchor="c", x=292, y=250)
        self.box_player_name.place(anchor="c", x=292, y=280)

        label_room_id = ttk.Label(
            self.frame,
            text="部屋番号を入力",
            foreground="#333f50",
            background="white",
            font=Game.font_jpn_bold,
        )
        self.box_room_id = ttk.Entry(self.frame, width=30)
        label_room_id.place(anchor="c", x=292, y=330)
        self.box_room_id.place(anchor="c", x=292, y=360)

        label_mode = ttk.Label(
            self.frame,
            text="モードを選択(auto: 1 / manual: 0)",
            foreground="#333f50",
            background="white",
            font=Game.font_jpn_bold,
        )
        self.box_mode = ttk.Entry(self.frame, width=30)
        label_mode.place(anchor="c", x=292, y=410)
        self.box_mode.place(anchor="c", x=292, y=440)

        label_achievments = ttk.Label(
            self.frame,
            text="Achievements",
            foreground="#333f50",
            background="white",
            font=Game.font_eng,
        )
        label_achievments.place(anchor="c", x=573, y=250)
        achievements = get_save()
        for i, k in enumerate(achievements.items()):
            if not isinstance(k[1], bool):
                label_content = ttk.Label(
                    self.frame,
                    text=k[0] + ":" + str(k[1]),
                    background="white",
                    font=Game.font_jpn,
                )
                label_content.place(anchor="c", x=573, y=290 + 30 * i)

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
            room_id=room_id, player_name=self.box_player_name.get(), mode=mode,
        )
        Game.player._api_com.enter_room()
        Game.show_waiting_disp()


class DispRegisterNum(Disp):
    def __init__(self) -> None:
        super().__init__()

        self.bg_image = tk.PhotoImage(
            file=os.path.join("img", "back", "hidden_input.png")
        )
        label_bg = tk.Label(
            master=self.frame, image=self.bg_image, width=800, height=600
        )
        label_bg.place(x=0, y=0)

        label = ttk.Label(
            self.frame,
            text="相手が当てる番号を入力",
            foreground="#333f50",
            background="white",
            font=Game.font_jpn_bold,
        )

        self.combos = []
        for i in range(5):
            self.combos.append(ttk.Combobox(
                self.frame,
                width=2,
                justify="center",
                foreground="#333f50",
                state="readonly",
                values=CHOICES,
                font=Game.font_eng_num,
            ))
            self.combos[i].place(anchor="c", x=280+i*60, y=300)


        label.place(anchor=tk.CENTER, x=400, y=270)

        button_enter = tk.Button(
            self.frame,
            highlightbackground="#ffffff",
            width=166,
            height=33,
            image=self.start_image,
            command=self.onclick,
        )
        button_enter.place(anchor="c", x=400, y=355)

    def onclick(self):
        """自身の数字登録画面でEnterが押された時の処理
        入力されている数字が正しければ、サーバに登録し、モードに応じた画面に移行
        そうでなければ入力ボックスを空にする
        :param なし
        :return: なし
        """
        if self.is_correct_num():
            hidden_num = ""
            for i in range(5):
                hidden_num += self.combos[i].get()
            Game.player._api_com.post_hidden(hidden_num)

            if Game.player.mode:
                Game.show_playing_auto_disp()
            else:
                Game.show_playing_manual_disp()
        else:
            for i in range(5):
                self.combos[i].delete(0, 1)

    def is_correct_num(self):
        """入力された数字を取得し、それが16進5桁の数字かどうか判定
        :param なし
        :rtype: bool
        :return: 16進5桁の数字ならTrue, そうでなければFalse
        """
        num = ""
        for i in range(5):
            num += self.combos[i].get()
        if len(num) == 5 and len(set(num)) == 5:
            return True
        return False


class DispPlayingManual(Disp):
    def __init__(self) -> None:
        super().__init__()
        self.bg_image = tk.PhotoImage(file=os.path.join("img", "back", "match.png"))
        label_bg = tk.Label(
            master=self.frame, image=self.bg_image, width=800, height=600
        )
        label_bg.place(x=0, y=0)

        
        self.combos = []
        for i in range(5):
            self.combos.append(ttk.Combobox(
                self.frame,
                width=2,
                justify="center",
                foreground="#333f50",
                state="readonly",
                values=CHOICES,
                font=Game.font_eng_num,
            ))
            self.combos[i].place(anchor="c", x=170+i*69, y=550)

        self.button = tk.Button(
            self.frame,
            highlightbackground="#ffffff",
            width=150,
            height=33,
            image=self.send_image,
            command=self.onclick,
            state=tk.NORMAL,
        )
        self.button.place(x=527, y=531)

        self.y_interval = 20
        self.y_you_guess = 13
        self.y_you_response = 13
        self.y_opponent_guess = 13
        self.y_opponent_response = 13
        self.canvas_you_guess = tk.Canvas(
            self.frame, width=120, height=300, borderwidth=0, bg="#2eb280"
        )
        self.canvas_you_guess.place(anchor=tk.CENTER, x=162, y=335)
        self.canvas_you_response = tk.Canvas(
            self.frame, width=120, height=300, borderwidth=0, bg="#2eb280"
        )
        self.canvas_you_response.place(anchor=tk.CENTER, x=315, y=335)

        self.canvas_opponent_guess = tk.Canvas(
            self.frame, width=120, height=300, borderwidth=0, bg="#009e9a"
        )
        self.canvas_opponent_guess.place(anchor=tk.CENTER, x=495, y=335)

        self.canvas_opponent_response = tk.Canvas(
            self.frame, width=120, height=300, borderwidth=0, bg="#009e9a"
        )
        self.canvas_opponent_response.place(anchor=tk.CENTER, x=645, y=335)

        # ここで、15枚、レスポンスに応じた画像を用意して、辞書形式にまとめておく
        photo_dir = os.path.join("img", "response", "")
        self.img_response_dict = {
            name[-13:-4]: ImageTk.PhotoImage(Image.open(name))
            for name in glob.glob(photo_dir + "*.png")
        }

        # 相手のテーブル作成用
        self.cnt_opponent_guess = 0

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
                label_turn = ttk.Label(
                    self.frame,
                    text="   YOU  ",
                    foreground="#333f50",
                    background="#96e9cc",
                    width=10,
                    font=Game.font_eng,
                )
                label_turn.place(anchor="c", x=288, y=63)

                opponent_table = Game.player.get_opponent_table()
                if self.cnt_opponent_guess < len(opponent_table):
                    latest_opponent_guess = opponent_table[-1]["guess"]
                    latest_opponent_res = (
                        opponent_table[-1]["hit"],
                        opponent_table[-1]["blow"],
                    )

                    self.canvas_opponent_guess.create_text(
                        60,
                        self.y_opponent_guess,
                        text=latest_opponent_guess,
                        fill="#ffffff",
                        font=("", 15, "bold"),
                    )
                    self.y_opponent_guess += self.y_interval
                    self.canvas_opponent_response.create_image(
                        60,
                        self.y_opponent_response,
                        image=self.img_response_dict[
                            str(latest_opponent_res[0])
                            + "hit"
                            + str(latest_opponent_res[1])
                            + "blow"
                        ],
                    )
                    self.y_opponent_response += self.y_interval

                    self.cnt_opponent_guess += 1
                self.button["state"] = tk.NORMAL
            else:
                label_turn = ttk.Label(
                    self.frame,
                    text="OPPONENT",
                    foreground="#333f50",
                    background="#96e9cc",
                    width=10,
                    font=Game.font_eng,
                )
                label_turn.place(anchor="c", x=288, y=63)
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
            guess_num = ""
            for i in range(5):
                guess_num += self.combos[i].get()
            self.canvas_you_guess.create_text(
                60,
                self.y_you_guess,
                text=guess_num,
                fill="#ffffff",
                font=("", 15, "bold"),
            )
            self.y_you_guess += self.y_interval

            guess_result = Game.player.post_guess_num(guess_num=guess_num)
            self.canvas_you_response.create_image(
                60,
                self.y_you_response,
                image=self.img_response_dict[
                    str(guess_result[0]) + "hit" + str(guess_result[1]) + "blow"
                ],
            )
            self.y_you_response += self.y_interval

        else:
            print("ERROR : unexpected number")

        for i in range(5):
            self.combos[i].delete(0, 1)

    def is_correct_num(self):
        """入力された数字を取得し、それが16進5桁の数字かどうか判定
        :param なし
        :rtype: bool
        :return: 16進5桁の数字ならTrue, そうでなければFalse
        """
        num = ""
        for i in range(5):
            num += self.combos[i].get()
        if len(num) == 5 and len(set(num)) == 5:
            return True
        return False


class DispPlayingAuto(Disp):
    def __init__(self) -> None:
        super().__init__()
        self.bg_image = tk.PhotoImage(file=os.path.join("img", "back", "match.png"))
        label_bg = tk.Label(
            master=self.frame, image=self.bg_image, width=800, height=600
        )
        label_bg.place(x=0, y=0)

        self.y_interval = 20
        self.y_you_guess = 13
        self.y_you_response = 13
        self.y_opponent_guess = 13
        self.y_opponent_response = 13
        self.canvas_you_guess = tk.Canvas(
            self.frame, width=120, height=300, borderwidth=0, bg="#20c080"
        )
        self.canvas_you_guess.place(anchor=tk.CENTER, x=162, y=335)
        self.canvas_you_response = tk.Canvas(
            self.frame, width=120, height=300, borderwidth=0, bg="#20c080"
        )
        self.canvas_you_response.place(anchor=tk.CENTER, x=315, y=335)

        self.canvas_opponent_guess = tk.Canvas(
            self.frame, width=120, height=300, borderwidth=0, bg="#40c0a0"
        )
        self.canvas_opponent_guess.place(anchor=tk.CENTER, x=495, y=335)

        self.canvas_opponent_response = tk.Canvas(
            self.frame, width=120, height=300, borderwidth=0, bg="#40c0a0"
        )
        self.canvas_opponent_response.place(anchor=tk.CENTER, x=645, y=335)

        # ここで、15枚、レスポンスに応じた画像を用意して、辞書形式にまとめておく
        photo_dir = os.path.join("img", "response", "")
        self.img_response_dict = {
            name[-13:-4]: ImageTk.PhotoImage(Image.open(name))
            for name in glob.glob(photo_dir + "*.png")
        }

        # 相手のテーブル作成用
        self.cnt_opponent_guess = 0

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

            opponent_table = Game.player.get_opponent_table()
            if self.cnt_opponent_guess < len(opponent_table):
                latest_opponent_guess = opponent_table[-1]["guess"]
                latest_opponent_res = (
                    opponent_table[-1]["hit"],
                    opponent_table[-1]["blow"],
                )

                self.canvas_opponent_guess.create_text(
                    60,
                    self.y_opponent_guess,
                    text=latest_opponent_guess,
                    fill="#ffffff",
                    font=("", 15, "bold"),
                )
                self.y_opponent_guess += self.y_interval

                self.canvas_opponent_response.create_image(
                    60,
                    self.y_opponent_response,
                    image=self.img_response_dict[
                        str(latest_opponent_res[0])
                        + "hit"
                        + str(latest_opponent_res[1])
                        + "blow"
                    ],
                )
                self.y_opponent_response += self.y_interval

                self.cnt_opponent_guess += 1

            guess_num = Game.player.auto_guess()
            self.canvas_you_guess.create_text(
                60,
                self.y_you_guess,
                text=guess_num,
                fill="#ffffff",
                font=("", 15, "bold"),
            )
            self.y_you_guess += self.y_interval

            guess_result = Game.player.post_guess_num(guess_num)
            self.canvas_you_response.create_image(
                60,
                self.y_you_response,
                image=self.img_response_dict[
                    str(guess_result[0]) + "hit" + str(guess_result[1]) + "blow"
                ],
            )
            self.y_you_response += self.y_interval

        elif game_state == 3:
            Game.show_reslut_disp()

        self.frame.after(self.check_interval, self.update_game_state)


class DispResult(Disp):
    def __init__(self) -> None:
        super().__init__()

        winner = Game.player.get_winner()
        Game.player.save_result(winner)
        if winner == Game.player._player_name:
            self.bg_image = tk.PhotoImage(
                file=os.path.join("img", "result", "VICTORY.png")
            )
        elif winner == None:
            self.bg_image = tk.PhotoImage(
                file=os.path.join("img", "result", "DRAW.png")
            )
        else:
            self.bg_image = tk.PhotoImage(
                file=os.path.join("img", "result", "DEFEAT.png")
            )

        label_result = tk.Label(
            master=self.frame, image=self.bg_image, width=800, height=600
        )
        label_result.place(x=0, y=0)
        self.button = tk.Button(
            self.frame,
            width=15,
            height=2,
            background="#20c080",
            text="FINISH GAME",
            font=("", 20, "bold"),
            foreground="#fff",
            command=self.onclick,
            anchor=tkinter.CENTER,
        )
        self.button.place(x=250, y=400)

    def onclick(self):
        Game.root.destroy()


def disp_test():
    root = tk.Tk()
    root.geometry("800x600")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frame = tk.Frame(root, bg="#555")
    frame.grid(row=0, column=0, sticky="nsew")

    button_image = tk.PhotoImage(file="img\kaji_kasaihouchiki_button.png").subsample(
        4, 4
    )
    buttons: List[tk.Button] = [None] * 16
    for i in range(16):
        buttons[i] = tk.Button(
            frame,
            width=80,
            height=80,
            image=button_image,
            text="b{}".format(hex(i)[2:]),
        )

        buttons[i].place(x=int(i % 4) * 90 + 430, y=int(i / 4) * 90 + 200)

    root.mainloop()


if __name__ == "__main__":

    disp_test()
