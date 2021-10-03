import random
from typing import List, Tuple

class AutoGuess:
    """自動推測クラス
    基本的にguess(guesss_num_prev, guess_result_prev)を呼び出すだけ
    :self._possible_answers List[str] : 答えとなりうる数字のリスト
    :self._guess_history : 過去に推測した数字のリスト
    :self._guess_result_history : 過去に推測した数字の結果のリスト
    :self._cnt int : 推測した回数 
    """
    def __init__(self) -> None:
        self._possible_answers: List[str] = self._make_all_number_list()
        self._guess_history: List[str] = []
        self._guess_result_history: List[Tuple[int, int]] = []
        self._cnt: int = 0

    def _make_all_number_list(self) -> List[str]:
    
        """全ての候補を取得
        :return List[str]: 取りうる全ての答え(524160通り)
        """
        ret = ["*****"] * 524160
        cnt_roop = 0

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
                            ret[cnt_roop] = (
                                hex(i)[2:]
                                + hex(j)[2:]
                                + hex(k)[2:]
                                + hex(l)[2:]
                                + hex(m)[2:]
                            )
                            cnt_roop += 1

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

    def guess(
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
