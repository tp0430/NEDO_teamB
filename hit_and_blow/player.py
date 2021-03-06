from logging import getLogger
import random
import time
import os
import json
import threading

from tkinter.constants import NO
from typing import Tuple, List
import numpy as np
from requests.exceptions import RequestException

from communication import APICom
from auto_guess import AutoGuess

ANS_LEN: int = 5
MIN_ANS: int = 0
MAX_ANS: int = 15

logger = getLogger("hit_and_blow").getChild("player")
class Player:
    """プレイ用モジュール。
    :param int _room_id: ルームID
    :param str _player_name: プレーヤー名
    :param APICom _api_com: APIComクラスの通信用オブジェクト
    :param int mode: 0->マニュアルモード(デフォルト), 1->自動対戦モード
    :param List[Tuple(str, Tuple(int, int))] guess_history: 対戦履歴, 初期値は[None, None]
    :param auto_guesser AutoGuess: 自動推測用オブジェクト, modeが0ならNone
    """
    def gen_random_num() -> str:
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

    def __init__(self, room_id: int, player_name: str, mode: int = 0, strength= 10, hidden_num = None) -> None:
        """コンストラクタ
        :param int room_id: ルームID
        :param str player_name: プレーヤー名
        :rtype: None
        :return: なし
        """

        self._player_name: str = player_name
        self._api_com: APICom = APICom(player_name=self._player_name, room_id=room_id)
        self.mode = mode

        self.guess_history: List[Tuple(str, Tuple(int, int))] = [(None, None)]
        if mode:
            self.auto_guesser = AutoGuess(strength= get_save()["レート"])

        self.json_path = os.path.join("save", "save.json")
        self._saved = False

        self.table = None
        self.update_interval = 0.1

        self._hidden_num = hidden_num

    def save_result(self, winner, lose_weight=3, weight=0.4):
        if not self._saved:
            with open(self.json_path, mode="r", encoding="utf-8") as f:
                json_load = json.load(f)
            
            json_load["game_count"]["プレイ回数"] += 1
            prev_ave_num = json_load["internal"]["平均回答回数"]
            this_num = len(self.guess_history) - 1

            if winner == self._player_name:
                json_load["game_count"]["勝利回数"] += 1
                if prev_ave_num == 0:
                    json_load["internal"]["平均回答回数"] = this_num
                else:
                    json_load["internal"]["平均回答回数"] = (1 - weight) * prev_ave_num + weight * this_num
            elif winner == None:
                json_load["game_count"]["引き分け回数"] += 1
                if prev_ave_num == 0:
                    json_load["internal"]["平均回答回数"] = this_num
                else:
                    json_load["internal"]["平均回答回数"] = (1 - weight) * prev_ave_num + weight * this_num
            else:
                json_load["game_count"]["敗北回数"] += 1
                if prev_ave_num == 0:
                    json_load["internal"]["平均回答回数"] = this_num + lose_weight
                else:
                    json_load["internal"]["平均回答回数"] = (1 - weight) * prev_ave_num + weight * (this_num + lose_weight)

            json_load["game_count"]["レート"] = round(np.exp((60-json_load["internal"]["平均回答回数"])/22.2), 2)
            if json_load["game_count"]["レート"] > 10:
                json_load["game_count"]["レート"] = 10
            if json_load["game_count"]["レート"] < 1:
                json_load["game_count"]["レート"] = 1

            json_load["internal"]["平均回答回数"] = round(json_load["internal"]["平均回答回数"], 2)

            if json_load["game_count"]["勝利回数"] ==1 and json_load["game_count"]["win_1"] == True:
                json_load["game_count"]["win_1"] == False
                pass #「初勝利」とか？
            elif json_load["game_count"]["敗北回数"] ==1 and json_load["game_count"]["lose_1"] == True:
                json_load["game_count"]["lose_1"] == False
                pass #「初敗北」とか？
            elif json_load["game_count"]["引き分け回数"] ==1 and json_load["game_count"]["draw_1"] == True:
                json_load["game_count"]["draw_1"] == False
                pass #「初引き分け」とか？
            elif json_load["game_count"]["勝利回数"] ==10 and json_load["game_count"]["win_10"] == True:
                json_load["game_count"]["win_10"] == False
                pass #「祝10勝」とか？
            elif json_load["game_count"]["敗北回数"] ==10 and json_load["game_count"]["lose_10"] == True:
                json_load["game_count"]["lose_10"] == False
                pass #「不屈の精神」とか？
            elif json_load["game_count"]["引き分け回数"] ==10 and json_load["game_count"]["draw_10"] == True:
                json_load["game_count"]["draw_10"] == False
                pass #「泥試合」とか？
            with open(self.json_path, mode="w", encoding="utf-8") as f:
                json.dump(json_load, f, ensure_ascii=False, indent=2)
                
            self._saved = True
    

    def is_my_turn(self) -> bool:
        """自分のターンかどうかを返す
        :param なし
        :rtype: bool
        :return: 自分のターンならTrue, 相手のターンならFalse
        """
        return self.table["now_player"] == self._player_name
    
    def get_state(self) -> int:
        """ゲームの状態を取得
        :param なし
        :rtype: int
        :return: 1: ゲーム未開始 , 2: 進行中 , 3: ゲーム終了
        """        
        return self.table["state"]
    
    def get_opponent_table(self) -> List:
        """相手のテーブルを取得
        :param なし
        :rtype: List[dict[]]
        :return: 相手のテーブル
        """   
        return self.table["opponent_table"]
    
    def auto_guess(self) -> str:
        """自動推測結果を返す
        :param なし
        :rtype: str
        :return: 自動推測した数字
        """   
        return self.auto_guesser.guess(self.guess_history[-1][0], self.guess_history[-1][1])
    
    def update_table(self) -> None:

        while True:
            try:
                self.table = self._api_com.get_table()
                if self.table.get("state") == 3:
                    break
                time.sleep(self.update_interval)
            except RequestException:
                time.sleep(1)
        return

    
    def enter_room(self) -> int:
        """対戦部屋に入室
        :param なし
        :rtype: int
        :return: status code
        """  
        return self._api_com.enter_room()

    def post_hidden_num(self, hidden_num) -> int:
        """自身の数字を登録
        :param 登録する数字
        :rtype: int
        :return: status code
        """  
        res = self._api_com.post_hidden(hidden_number= hidden_num)
        if self.mode != 2:
            self.thread = threading.Thread(target= self.update_table)
            self.thread.setDaemon(True)
            self.thread.start()
        return res

    def post_guess_num(self, guess_num: str) -> Tuple[int, int]:
        """推測した数字をサーバに上げる
        推測した数字とその結果はhistoryに内部で追加している
        :param　str: 推測した数字
        :rtype: Tuple[int, int]
        :return: 推測結果[hit, blow]
        """  
        guess_result: Tuple[int, int] = None

        self._api_com.post_guess(guess_number=guess_num)
        latest_result = self._api_com.get_table()["table"][-1]
        guess_result = (latest_result["hit"], latest_result["blow"])


        self.guess_history.append((guess_num, guess_result))

        return guess_result
    
    def get_winner(self):
        """勝者を取得
        :param　str: なし
        :rtype: str
        :return: 勝者のplayer_name
        """  
        return self.table["winner"]
    
    def play_game_internal(self):
        """内部でゲームをプレイする関数
        :param　: なし
        :rtype: 
        :return: なし
        """        
        logger.debug("内部でプレイを開始します。")

        while True:
            try:
                self.enter_room()
                break
            except RequestException:
                logger.error("cpの入室に失敗しました。再度試します。")
                time.sleep(0.5)

        while True:
            try:
                state = self._api_com.get_game_state()
                if state == 2:
                    break
            except RequestException:
                logger.error("テーブルの取得に失敗しました。再度試します。")
                pass
            time.sleep(0.5)

        if self._hidden_num == None:
            mynum = Player.gen_random_num()
        else:
            mynum = self._hidden_num

        while True:
            try:
                self.post_hidden_num(mynum)
                logger.debug(mynum)
                break
            except RequestException:
                logger.error("自身の数字の登録に失敗しました。再度ポストします。")
                time.sleep(0.5)

        while True:
            try:
                table = self._api_com.get_table()
            except RequestException:
                logger.error("テーブルの取得に失敗しました。再度試します。")
                time.sleep(0.5)
                continue

            if table["now_player"] == self._player_name and table["state"] != 3:
                try:
                    self.post_guess_num(self.auto_guess())
                except RequestException:
                    logger.error("推測した数字の登録に失敗しました。再度試します。")
                    time.sleep(0.5)
            if table["state"] == 3:
                break
            time.sleep(0.5)
        
        print("my number is {}".format(mynum))

def get_save():
    
    json_path = os.path.join("save", "save.json")
    if not os.path.exists("save"):
        logger.debug("ファイルが存在しません。新しく作ります。")
        os.makedirs("save")
        init_save = {
            "game_count": {
                "レート": 1,
                "プレイ回数": 0,
                "勝利回数": 0,
                "敗北回数": 0,
                "引き分け回数": 0,
                "win_1": True,
                "lose_1": True,
                "draw_1": True,
                "win_10": True,
                "lose_10": True,
                "draw_10": True,
            },
            "internal": {
                "平均回答回数": 0
            }
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(init_save, f, ensure_ascii=False)
    with open(json_path, "r", encoding="utf-8") as f:
        json_load = json.load(f)
    return json_load["game_count"]

