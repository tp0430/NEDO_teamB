import random
import time
from tkinter.constants import NO
from typing import Tuple, List

from communication import APICom
from auto_guess import AutoGuess

import tkinter as tk
import tkinter.ttk as ttk


ANS_LEN: int = 5
MIN_ANS: int = 0
MAX_ANS: int = 15


class Player:
    """プレイ用モジュール。
    :param int _room_id: ルームID
    :param str _player_name: プレーヤー名
    :param APICom _api_com: APIComクラスの通信用オブジェクト
    :param int mode: 0->マニュアルモード(デフォルト), 1->自動対戦モード
    :param List[Tuple(str, Tuple(int, int))] guess_history: 対戦履歴, 初期値は[None, None]
    :param auto_guesser AutoGuess: 自動推測用オブジェクト, modeが0ならNone
    """

    def __init__(self, room_id: int, player_name: str, mode: int = 0) -> None:
        """コンストラクタ
        :param int room_id: ルームID
        :param str player_name: プレーヤー名
        :rtype: None
        :return: なし
        """

        self._room_id: int = room_id
        self._player_name: str = player_name
        self._api_com: APICom = APICom(
            player_name=self._player_name, room_id=self._room_id
        )
        self.mode: int = mode
        self.guess_history: List[Tuple(str, Tuple(int, int))] = [(None, None)]
        if mode:
            self.auto_guesser = AutoGuess()

    def is_my_turn(self) -> bool:
        """自分のターンかどうかを返す
        :param なし
        :rtype: bool
        :return: 自分のターンならTrue, 相手のターンならFalse
        """
        return (self._api_com.get_table()["state"] == 2) and (
            self._api_com.get_table()["now_player"] == self._player_name
        )

    def get_state(self) -> int:
        """ゲームの状態を取得
        :param なし
        :rtype: int
        :return: 1: ゲーム未開始 , 2: 進行中 , 3: ゲーム終了
        """
        return self._api_com.get_table()["state"]

    def auto_guess(self) -> str:
        """自動推測結果を返す
        :param なし
        :rtype: str
        :return: 自動推測した数字
        """
        return self.auto_guesser.guess(
            self.guess_history[-1][0], self.guess_history[-1][1]
        )

    # 戻り値悩み中、boolで返すのが後々楽そうなので要編集
    def enter_room(self) -> bool:
        """対戦部屋に入室
        :param なし
        :rtype: bool
        :return: 部屋に入れたかどうか
        """
        return self._api_com.enter_room()

    def post_guess_num(self, guess_num: str) -> Tuple[int, int]:
        """推測した数字をサーバに上げる
        :param　str: 推測した数字
        :rtype: Tuple[int, int]
        :return: 推測結果[hit, blow]
        """
        guess_result: Tuple[int, int] = None

        self._api_com.post_guess(guess_number=guess_num)
        latest_result = self._api_com.get_table()["table"][-1]
        guess_result = (latest_result["hit"], latest_result["blow"])

        print("{} : {}".format(guess_num, guess_result))

        self.guess_history.append((guess_num, guess_result))

        return guess_result

    def get_winner(self):
        """勝者を取得
        :param　str: なし
        :rtype: str
        :return: 勝者のplayer_name
        """
        return self._api_com.get_table()["winner"]

