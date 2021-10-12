import random
import time
from typing import Tuple, List

from communication import APICom
from auto_guess import AutoGuess

ANS_LEN: int = 5
MIN_ANS: int = 0
MAX_ANS: int = 15
REPEAT_NUM: int = 100
PLAYER_NAME: str = "B"
FIRST_ROOM_ID: int = 1  # 上野さん、対戦時に設定してください。


class Player_auto:
    """プレイ用モジュール。
    :param bool _is_start_game: ゲームが開始できているか。
    :param bool _is_end_game: ゲームが終了しているか。
    :param str _player_name: プレーヤー名
    :param int _room_id: ルームID
    :param str _hidden_number: 相手が当てる数字
    :param APICom _api_com: APIComクラスの通信用オブジェクト
    :param int mode: 0->マニュアルモード(デフォルト), 1->自動対戦モード
    """

    def __init__(
        self, room_id: int, player_name: str, mode: int = 0, strength=10
    ) -> None:
        """コンストラクタ
        :param int room_id: ルームID
        :param str player_name: プレーヤー名
        :rtype: None
        :return: なし
        """
        self.strength = strength
        self._is_start_game: bool = False
        self._is_end_game: bool = False
        self._room_id: int = room_id
        self._player_name: str = player_name
        self._api_com: APICom = APICom(
            player_name=self._player_name, room_id=self._room_id
        )
        self._hidden_number = self._random_maker()

    def _init_game(self) -> None:
        """ゲーム開始の作業をひとまとめにした関数。
        ゲーム開始が確認されたら、self._start_gameがTrueになる。
        :param: なし
        :rtype: None
        :return: なし
        """
        time.sleep(0.2)
        _ = self._api_com.enter_room()

        while self._api_com.get_room()["state"] == 1:
            time.sleep(0.2)
        print(self._hidden_number)
        #APIの処理待ち
        time.sleep(0.2)
        self._api_com.post_hidden(hidden_number=self._hidden_number)
        self._is_start_game = True
        return

    def _random_maker(self) -> str:
        choices = [
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
        return_str = ""
        while True:
            new = random.choice(choices)
            if new not in return_str:
                return_str += new
            if len(return_str) == 5:
                return return_str

    def _proceed_game_auto(self) -> None:
        """オートモードでのゲーム中の操作をひとまとめにした関数。
        ゲーム終了が確認されると、self._end_gameがTrueになる。
        :param: なし
        :rtype: None
        :return: なし
        """

        guess_program = AutoGuess(strength=self.strength)

        guess_num: str = None
        guess_result: Tuple[int, int] = None
        while self._api_com.get_table()["state"] == 2:

            table = self._api_com.get_table()
            if table["now_player"] == self._player_name:

                guess_num = guess_program.guess(guess_num, guess_result)
                self._api_com.post_guess(guess_number=guess_num)
                latest_result = self._api_com.get_table()["table"][-1]
                guess_result = (latest_result["hit"], latest_result["blow"])
        
            time.sleep(0.5)
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
            return "win"
        elif winner == None:
            return "draw"
        else:
            return "lose"

    def play_game(self) -> None:
        """ゲーム開始から終了までの一連の流れ
        :param: なし
        :rtype: None
        :return: なし
        """
        self._init_game()
        if self._is_start_game == True:
            self._proceed_game_auto()
            if self._is_end_game == True:
                result: str = self._show_result()
                return result


def main(first_room_id=FIRST_ROOM_ID, repeat_num=REPEAT_NUM):

    results = {"win": 0, "draw": 0, "lose": 0}
    for i in range(repeat_num):
        player = Player_auto(room_id=first_room_id + i, player_name=PLAYER_NAME)
        results[player.play_game()] += 1
    print(results)

    return


if __name__ == "__main__":
    main(FIRST_ROOM_ID)
