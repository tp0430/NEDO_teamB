import random
import time
from typing import Tuple, List

from communication import APICom
from auto_guess import AutoGuess

import streamlit as st

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
        self._is_start_game: bool = False
        self._is_end_game: bool = False
        self._room_id: int = room_id
        self._player_name: str = player_name
        self._hidden_number: str = st.text_input("Enter hidden number")
        self._api_com: APICom = APICom(
            player_name=self._player_name, room_id=self._room_id
        )
        self.mode: int = mode

    def _init_game(self) -> None:
        """ゲーム開始の作業をひとまとめにした関数。
        ゲーム開始が確認されたら、self._start_gameがTrueになる。
        :param: なし
        :rtype: None
        :return: なし
        """

        _ = self._api_com.enter_room()

        display_waiting = False

        while self._api_com.get_room()["state"] == 1:
            if display_waiting == False:
                st.write("now waiting opponent")
                display_waiting = True
            time.sleep(5)
        self._api_com.post_hidden(hidden_number=self._hidden_number)
        self._is_start_game = True
        return

    def _proceed_game_manual(self) -> None:
        """マニュアルモードでのゲーム中の操作をひとまとめにした関数。
        ゲーム終了が確認されると、self._end_gameがTrueになる。
        :param: なし
        :rtype: None
        :return: なし
        """

        guess_num: str = None
        guess_result: Tuple[int, int] = None
        guess_num = st.text_input("enter guess number")
        while self._api_com.get_table()["state"] == 2:
            table = self._api_com.get_table()
            if table["now_player"] == self._player_name:
                self._api_com.post_guess(guess_number=guess_num)
                latest_result = self._api_com.get_table()["table"][-1]
                guess_result = (latest_result["hit"], latest_result["blow"])
                st.write("{} : {}".format(guess_num, guess_result))
            time.sleep(1)
        self._is_end_game = True
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

                st.write("{} : {}".format(guess_num, guess_result))

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
            st.write("YOU WIN!")
        elif winner == None:
            st.write("DRAW")
        else:
            st.write("YOU LOSE")
        return

    def play_game(self) -> None:
        """ゲーム開始から終了までの一連の流れ
        :param: なし
        :rtype: None
        :return: なし
        """
        self._init_game()
        if self._is_start_game == True and len(self._hidden_number) != 0:
            st.write("Game Start")

            if self.mode:
                self._proceed_game_auto()
            else:
                self._proceed_game_manual()
            if self._is_end_game == True:
                self._show_result()
                return


"""
テストはtestsの中に書く

# 性能テスト
if __name__ == "__main__":

    repetition = 100
    times_to_correct = {}

    # 処理速度計測
    time_start = time.time()

    for i in range(repetition):
        auto_player = AutoPlayer()
        ans = make_number_random()
        # print("ans---{}".format(ans))

        guess_num = None
        guess_result = None
        while 1:
            

            guess_num = auto_player.guess(guess_num, guess_result)
            guess_result = hit_and_blow(guess_num, ans)
            # print("{} : {}".format(guess_num, guess_result))
            # print(len(auto_player.possible_answers))

            if guess_result[0] == 5:

                # if auto_player.cnt in times_to_correct:
                #     times_to_correct[auto_player.cnt] += 1
                # else:
                #     times_to_correct[auto_player.cnt] = 1
                # print("game finish!, {} times".format(auto_player.cnt))
                break
    
    processing_time = time.time() - time_start

    times_to_correct = sorted(times_to_correct.items())
    print(times_to_correct)
    print("time to finish this process {} times : {}".format(repetition, processing_time))
"""
