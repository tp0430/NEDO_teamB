import random
from typing import List, Tuple

class AutoGuess:
    """自動推測クラス
    :param strenth int: 自動推測の強さ, 最大10, 最小1
    基本的にguess(guesss_num_prev, guess_result_prev)を呼び出すだけ
    :self._possible_answers List[str] : 答えとなりうる数字のリスト
    :self._guess_history : 過去に推測した数字のリスト
    :self._guess_result_history : 過去に推測した数字の結果のリスト
    :self._cnt int : 推測した回数 
    """
    def __init__(self, strength : float = 10) -> None:
        self._possible_answers: List[str] = self._make_all_number_list()
        self.cnt: int = 0
        self._strength = strength

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

        if guess_num != None:
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

        #最初の推測ではnarrow_guess_num_list()は呼ぶようにする。
        #最初50万通りあるので、弱い設定でもこれはへらしておきたい。

        if (self.cnt == 0) or (random.uniform(0, 10) <= self._strength):
            self._narrow_guess_num_list(guess_num= guess_num_prev, guess_result= guess_result_prev)

        self.cnt += 1
        return self._select_guess_num()


def test_autoguess(repetition : int, strenth : int = 10):

    import time

    def get_random_num():
        ret = ""
        while True:
            digit = hex(random.randint(0, 15))[2:]
            if digit in ret:
                continue
            else:
                ret += digit
            if len(ret) == 5:
                break
        return ret

    def hit_and_blow(guess: str, ans: str) -> Tuple[int, int]:
        hit = 0
        blow = 0
        for i in range(len(guess)):
            if guess[i] == ans[i]:
                hit += 1
        blow = len(set(guess) & set(ans)) - hit

        return (hit, blow)

    repetition_result = {}

    time_start = time.time()

    
    for i in range(repetition):
        auto_guess = AutoGuess(strenth= strenth)
        answer_num = get_random_num()
        guess_num = None
        guess_result = None

        while True:
            guess_num = auto_guess.guess(guess_num_prev= guess_num, guess_result_prev= guess_result)
            guess_result = hit_and_blow(guess= guess_num, ans= answer_num)

            if guess_result[0] == 5:
                break
        repetition_result[auto_guess.cnt] = repetition_result.get(auto_guess.cnt, 0) + 1
    
    elapsed_time = time.time() - time_start
    
    # result = sorted(repetition_result.keys())
    
    print("finish {} times process, in {} sec".format(repetition, elapsed_time))
    # for item in result:
    #     print(item)
    print(repetition_result)

if __name__ == "__main__":
    test_autoguess(10, 8)

