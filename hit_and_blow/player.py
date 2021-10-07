import random
import time
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
    :param bool _is_start_game: ゲームが開始できているか。
    :param bool _is_end_game: ゲームが終了しているか。
    :param str _player_name: プレーヤー名
    :param int _room_id: ルームID
    :param str _hidden_number: 相手が当てる数字
    :param APICom _api_com: APIComクラスの通信用オブジェクト
    :param int mode: 0->マニュアルモード(デフォルト), 1->自動対戦モード
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
        self._hidden_number: str
        self._api_com: APICom = APICom(
            player_name=self._player_name, room_id=self._room_id
        )
        self.mode: int = mode

        self.guess_num = None
            
    def set_hidden_num(self, num):
        self._hidden_number = num
    
    def is_my_turn(self):
        return (self._api_com.get_table()["state"] == 2 ) and (self._api_com.get_table()["now_player"] == self._player_name)
    
    def init_game(self) -> None:
        """入室、数字の登録
        :param: なし
        :rtype: None
        :return: なし
        """

        self._api_com.enter_room()
        self._api_com.post_hidden(hidden_number=self._hidden_number)
        return
    
    def check_game_state(self) -> int:
        return self._api_com.get_table()["state"] 

    def post_guess_num(self, guess_num: str):
        guess_result: Tuple[int, int] = None

        game_state = self._api_com.get_table()["state"] 

        if game_state == 2:

            self._api_com.post_guess(guess_number=guess_num)
            latest_result = self._api_com.get_table()["table"][-1]
            guess_result = (latest_result["hit"], latest_result["blow"])

            print("{} : {}".format(guess_num, guess_result))

        return

    def _proceed_game_auto(self) -> None:
        """オートモードでのゲーム中の操作をひとまとめにした関数。
        ゲーム終了が確認されると、self._end_gameがTrueになる。
        :param: なし
        :rtype: None
        :return: なし
        """

        guess_program = AutoGuess()

        guess_num: str = None
        guess_result: Tuple[int, int] = None
        while self._api_com.get_table()["state"] == 2:

            table = self._api_com.get_table()
            if table["now_player"] == self._player_name:

                guess_num = guess_program.guess(guess_num, guess_result)
                self._api_com.post_guess(guess_number=guess_num)
                latest_result = self._api_com.get_table()["table"][-1]
                guess_result = (latest_result["hit"], latest_result["blow"])

                print("{} : {}".format(guess_num, guess_result))

            time.sleep(1)
        self._is_end_game = True
        return

    def _show_result(self) -> None:
        """対戦結果を表示する。
        :param: なし
        :rtype: None
        :return: なし
        """

        winner = self._api_com.get_table()["winner"]
        if winner == self._player_name:
            print("YOU WIN!")
        elif winner == None:
            print("DRAW")
        else:
            print("YOU LOSE")
        return

    def play_game(self) -> None:
        """ゲーム開始から終了までの一連の流れ
        :param: なし
        :rtype: None
        :return: なし
        """

        if self._is_start_game == True:
            print("GAME START!")

            if self.mode:
                self._proceed_game_auto()
            else:
                self._proceed_game_manual()
            if self._is_end_game == True:
                self._show_result()
                return


def main():

    pass



if __name__ == "__main__":

    main()
