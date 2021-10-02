import random
import time
from typing import Tuple, List

from communication import APICom


ANS_LEN: int = 5
MIN_ANS: int = 0
MAX_ANS: int = 15


class ManualPlayer:
    """手動プレイ用モジュール。
    :param bool _start_game: ゲームが開始できているか。
    :param bool _end_game: ゲームが終了しているか。
    :param str _player_name: プレーヤー名
    :param int _room_id: ルームID
    :param str _hidden_number: 相手が当てる数字
    :param APICom _api_com: APIComクラスの通信用オブジェクト
    """

    def __init__(self, room_id: int, player_name: str) -> None:
        """コンストラクタ
        :param int room_id: ルームID
        :param str player_name: プレーヤー名
        :rtype: None
        :return: なし
        """

        self._start_game: bool = False
        self._end_game: bool = False
        self._player_name: str = player_name
        self._room_id: int = room_id
        self._hidden_number: str = input("enter hidden number : ")
        self._api_com: APICom = APICom(
            player_name=self._player_name, room_id=self._room_id
        )

    def _init_game(self) -> None:
        """ゲーム開始の作業をひとまとめにした関数。
        ゲーム開始が確認されたら、self._start_gameがTrueになる。
        :param: なし
        :rtype: None
        :return: なし
        """

        _ = self._api_com.enter_room()
        while self._api_com.get_room()["state"] == 1:
            print("now waiting opponent")
            time.sleep(5)
        self._api_com.post_hidden(hidden_number=self._hidden_number)
        self._start_game = True
        return

    def _proceed_game(self) -> None:
        """ゲーム中の操作をひとまとめにした関数。
        ゲーム終了が確認されると、self._end_gameがTrueになる。
        :param: なし
        :rtype: None
        :return: なし
        """
        guess_num: str = None
        guess_result: Tuple[int, int] = None
        while self._api_com.get_table()["state"] == 2:

            table = self._api_com.get_table()
            if table["now_player"] == self._player_name:

                guess_num = input("enter guess number : ")
                self._api_com.post_guess(guess_number=guess_num)
                latest_result = self._api_com.get_table()["table"][-1]
                guess_result = (latest_result["hit"], latest_result["blow"])

                print("{} : {}".format(guess_num, guess_result))

            time.sleep(1)
        self._end_game = True
        return

    def _show_result(self) -> None:
        """対戦結果を表示する。
        :param: なし
        :rtype: None
        :return: なし
        """

        # drawだった時の判定を拾えていない
        if self._api_com.get_table()["winner"] == self._player_name:
            print("YOU WIN!")
        else:
            print("YOU LOSE")
        return

    def play_game(self) -> None:
        """ゲーム開始から終了までの一連の流れ
        :param: なし
        :rtype: None
        :return: なし
        """
        self._init_game()
        if self._start_game == True:
            print("GAME START!")
            self._proceed_game()
            if self._end_game == True:
                self._show_result()
                return


class AutoPlayer(ManualPlayer):
    """手動プレイ用モジュール。
    :param bool _start_game: ゲームが開始できているか。
    :param bool _end_game: ゲームが終了しているか。
    :param str _player_name: プレーヤー名
    :param int _room_id: ルームID
    :param str _hidden_number: 相手が当てる数字
    :param APICom _api_com: APIComクラスの通信用オブジェクト
    :param List[str] _possible_answers: 答となりうる数字のリスト
    :param List[str] _guess_history: 推測履歴
    :param _guess_result_history: 推測した結果の履歴
    :param _cnt: 推測回数
    """
    def __init__(self, room_id, player_name) -> None:
        super(AutoPlayer, self).__init__(room_id, player_name)
        self._possible_answers: List[str] = self._make_all_number_list()
        self._guess_history: List[str] = []
        self._guess_result_history: List[Tuple[int, int]] = []
        self._cnt: int = 0

    def _make_all_number_list(self) -> List[str]:

        """全ての候補を取得
        :return List[str]: 取りうる全ての答え(524160通り)
        """
        ret = []

        for i in range(0x10):
            for j in range(0x10):
                if j == i:
                    continue
                for k in range(0x10):
                    if k == j or k == i:
                        continue
                    for l in range(0x10):
                        if l == k or l == j or l == i:
                            continue
                        for m in range(0x10):
                            if m == l or m == k or m == j or m == i:
                                continue
                            ret.append(
                                hex(i)[2:]
                                + hex(j)[2:]
                                + hex(k)[2:]
                                + hex(l)[2:]
                                + hex(m)[2:]
                            )

        return ret

    def _select_guess_num(self) -> str:
        """答の候補から一つ抽出
        :param なし
        :return str: 選ばれた数字
        """
        return random.choice(self._possible_answers)

    def _hit_and_blow(self, guess: str, ans: str) -> Tuple[int, int]:
        """hit&blowのゲーム。
        :param str guess: 予想した値。
        :param str ans: 正解の値(本来は相手のものは分からない)。
        :return Tuple[int, int]: hitとblowの値。
        """

        hit = 0
        blow = 0
        for i in range(len(guess)):
            if guess[i] == ans[i]:
                hit += 1
        blow = len(set(guess) & set(ans)) - hit

        return (hit, blow)

    def _narrow_guess_num_list(
        self, guess_num: str = None, guess_result: Tuple[int, int] = None
    ) -> int:

        """推測結果から候補の数を減らす。
        :param str guess_num: 推測した数字
        :param Tuple[int, int] guess_result: 推測した結果(hit, blow)
        :return int: 減らした後の候補数
        """

        if guess_num == None:
            guess_num = self._guess_history[-1]
        if guess_result == None:
            guess_result = self._guess_result_history[-1]

        self._possible_answers = [
            item
            for item in self._possible_answers
            if guess_result == self._hit_and_blow(guess=guess_num, ans=item)
        ]

        return len(self._possible_answers)

    def _guess(
        self, guess_num_prev: str = None, guess_result_prev: Tuple[int, int] = None
    ) -> str:

        """前回の推測結果から、次に推測すべき数字を決定
        :*param str guess_num_prev: 推測した数字
        :*param str guess_result_prev: 推測した結果(hit, blow)
        :return str: 次に推測すべき数字
        """

        self._cnt += 1

        if guess_num_prev != None:
            self._guess_history.append(guess_num_prev)
            self._guess_result_history.append(guess_result_prev)

            self._narrow_guess_num_list()

        return self._select_guess_num()

    def _proceed_game(self):
        # 継承元のproceed_gameを上書き
        guess_num = None
        guess_result = None
        while self._api_com.get_table()["state"] == 2:

            table = self._api_com.get_table()
            if table["now_player"] == self._player_name:

                guess_num = self._guess(guess_num, guess_result)
                self._api_com.post_guess(guess_number=guess_num)
                latest_result = self._api_com.get_table()["table"][-1]
                guess_result = (latest_result["hit"], latest_result["blow"])

                print("{} : {}".format(guess_num, guess_result))

            time.sleep(1)
        self._end_game = True
        return


def make_number_random() -> str:
    """ランダムな重複しない5つの数字を作る。
    :param: なし
    :return: 生成した文字列
    """

    char_list = [
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

    ret = ""
    while len(ret) != ANS_LEN:
        random_num = random.choice(char_list)
        if random_num not in ret:
            ret += random_num

    return ret


def hit_and_blow(guess: str, ans: str) -> Tuple[int, int]:
    """hit&blowのゲーム。
    :param str guess: 予想した値。
    :param str ans: 正解の値(本来は相手のものは分からない)。
    :return Tuple[int, int]: hitとblowの値。
    """

    hit = 0
    blow = 0
    for i in range(len(guess)):
        if guess[i] == ans[i]:
            hit += 1
    blow = len(set(guess) & set(ans)) - hit
    return (hit, blow)


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
