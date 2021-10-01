import random
import time
from typing import Sized, Tuple, List

ANS_LEN = 5
MIN_ANS = 0
MAX_ANS = 15

class Brain:

    def __init__(self) -> None:
        self.possible_answers = self.make_all_number_list()
        self.guess_history = []
        self.guess_result_history = []
        self.cnt = 0

    def make_all_number_list(self) -> List[str]:
        
        """全ての候補を取得
        :return List[str]
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
                            ret.append(hex(i)[2:] + hex(j)[2:] + hex(k)[2:] + hex(l)[2:] + hex(m)[2:])

        return ret

    def select_guess_num(self):
        return random.choice(self.possible_answers)

    def hit_and_blow(self, guess: str, ans: str) -> Tuple[int, int]:
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

    def narrow_guess_num_list(self, guess_num : str = None, guess_result : Tuple[int, int] = None) -> int:

        """推測結果から候補の数を減らす。
        :param str guess_num: 推測した数字
        :param Tuple[int, int] guess_result: 推測した結果(hit, blow)
        :return int: 減らした後の候補数
        """

        if guess_num == None:
            guess_num = self.guess_history[-1]
        if guess_result == None:
            guess_result = self.guess_result_history[-1]

        # 元のリストから一つずつ要素を削除するとO(n^2)の計算時間がかかるので、違うリストを用意して移す
        new_possible_answers = []

        for item in self.possible_answers:
            if guess_result == self.hit_and_blow(guess= guess_num, ans= item):
                new_possible_answers.append(item)

        self.possible_answers = new_possible_answers

        return len(self.possible_answers)

    def guess(self, guess_num_prev : str = None, guess_result_prev : Tuple[int, int] = None) -> str:

        """前回の推測結果から、次に推測すべき数字を決定
        :*param str guess_num_prev: 推測した数字
        :*param str guess_result_prev: 推測した結果(hit, blow)
        :return str: 次に推測すべき数字
        """

        self.cnt += 1

        if guess_num_prev != None:
            self.guess_history.append(guess_num_prev)
            self.guess_result_history.append(guess_result_prev)

            self.narrow_guess_num_list()

        return self.select_guess_num()

def make_number_random() -> str:
    """ランダムな重複しない5つの数字を作る。
    :param: なし
    :return: 生成した文字列
    """

    char_list = ["0" ,"1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

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

# 性能テスト
if __name__ == "__main__":

    repetition = 100
    times_to_correct = {}

    # 処理速度計測
    time_start = time.time()

    for i in range(repetition):
        brain = Brain()
        ans = make_number_random()
        # print("ans---{}".format(ans))

        guess_num = None
        guess_result = None
        while 1:
            

            guess_num = brain.guess(guess_num, guess_result)
            guess_result = hit_and_blow(guess_num, ans)
            # print("{} : {}".format(guess_num, guess_result))
            # print(len(brain.possible_answers))

            if guess_result[0] == 5:

                # if brain.cnt in times_to_correct:
                #     times_to_correct[brain.cnt] += 1
                # else:
                #     times_to_correct[brain.cnt] = 1
                # print("game finish!, {} times".format(brain.cnt))
                break
    
    processing_time = time.time() - time_start

    times_to_correct = sorted(times_to_correct.items())
    print(times_to_correct)
    print("time to finish this process {} times : {}".format(repetition, processing_time))


