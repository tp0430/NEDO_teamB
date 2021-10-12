# coding: UTF-8
"""
    * File name: communication.py
    * Description: APIを使った通信用のモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
    ---作りこむこと---
    1.room_idが入力された場合とそうでない場合の分岐
    2.APIからのstatus_codeが200でないときの例外処理
"""
import requests
from typing import Dict, Union, List
from logging import getLogger
logger = getLogger("hit_and_blow").getChild("communication")


class APICom:
    """通信用モジュール
    :param str URL:サーバのURL
    :param requests.sessions.Session session: session id
    :param str player_id: プレーヤーID
    :param dict HEADERS: ヘッダ
    :param str player_name: プレーヤー名
    :param int room_id: ルームID
    """

    def __init__(self, player_name: str, room_id: int):
        """
        :param str player_name:プレイヤー名
        :param int room_id:ルームID
        :rtype:None
        :return:なし
        """
        self._URL: str = "https://damp-earth-70561.herokuapp.com"
        self._session = requests.Session()
        self._HEADERS: Dict[str, str] = {"Content-Type": "application/json"}
        self._player_name: str = player_name
        self._player_id: str = ""
        if self._player_name == "B":
            self._player_id = "7d025351-7836-4904-a48f-f58019b6ca77"
        elif self._player_name == "B2":
            self._player_id = "a9c2784a-2279-4215-bc7d-1255dbdf911d"
        else:
            print("ここで例外を発生")
        self._room_id: int = room_id  # ここの値は2000~2999の範囲(使ってもいい部分)で都度変える。

    def get_rooms(self) -> dict:
        """全ての対戦部屋の情報を取得する.
        :rtype:dict
        :return: 全ての対戦部屋のURL
        """
        url_get_all_rooms = self._URL + "/rooms/"
        result = self._session.get(url_get_all_rooms)

        logger.debug("get rooms -> {}".format(result.status_code))
        result.raise_for_status()

        return result.json()

    def enter_room(self) -> int:
        """対戦部屋を作成し、指定したユーザを登録する。
        待機中の状態の対戦部屋が存在する場合は、指定したユーザを該当の対戦部屋のプレイヤーとして登録する。
        selfにルームIDを指定した場合は、該当のルームIDの対戦部屋にユーザを登録。
        :rtype:int
        :return: status code
        """
        url_enter_room = self._URL + "/rooms/"
        enter_room_json = {"player_id": self._player_id, "room_id": self._room_id}

        result = self._session.post(
            url_enter_room, headers=self._HEADERS, json=enter_room_json
        )

        logger.debug("enter room -> {}".format(result.status_code))
        result.raise_for_status()
        return result.status_code

    def get_room(self) -> dict:
        """指定した対戦部屋の情報を取得する
        :rtype:dict
        :return: 指定した対戦部屋のURL
        """
        url_get_room = self._URL + "/rooms/" + str(self._room_id)

        result = self._session.get(url_get_room)
        result.raise_for_status()
        return result.json()

    def get_table(self) -> dict:
        """対戦情報テーブル(現在のターン, hit&blowの履歴, 勝敗の判定)を取得する.
        :rtype:dict
        :return: 現在のターン，hit&blowの履歴，勝敗の判定
        """
        url_get_table = (
            self._URL
            + "/rooms/"
            + str(self._room_id)
            + "/players/"
            + self._player_name
            + "/table"
        )

        result = self._session.get(url_get_table)
        result.raise_for_status()
        return result.json()

    def post_hidden(self, hidden_number: str) -> dict:
        """相手が当てる5桁の16進数を登録する. ※アルファベットは小文字のみ
        :param str hidden_number: こちらが指定する答え
        :rtype:dict
        :return:{"プレイヤーID":"指定した答え"}
        """
        url_post_hidden = (
            self._URL
            + "/rooms/"
            + str(self._room_id)
            + "/players/"
            + self._player_name
            + "/hidden"
        )
        post_hidden_json = {
            "player_id": self._player_id,
            "hidden_number": hidden_number,
        }

        result = self._session.post(
            url_post_hidden, headers=self._HEADERS, json=post_hidden_json
        )

        logger.debug("post hidden number: status code : {}".format(result.status_code))
        result.raise_for_status()
        return result.status_code

    def post_guess(self, guess_number: str) -> int:
        """推測した数字を登録する
        :param str guess_number: 推測した数値
        :rtype:dict
        :return:{"プレイヤーID":"推測した答え"}
        """
        url_post_guess = (
            self._URL
            + "/rooms/"
            + str(self._room_id)
            + "/players/"
            + self._player_name
            + "/table/guesses"
        )
        post_guess_json = {"player_id": self._player_id, "guess": guess_number}

        result = self._session.post(
            url_post_guess, headers=self._HEADERS, json=post_guess_json
        )

        logger.debug(str(result.status_code))
        result.raise_for_status()
        return result.status_code

    def get_game_state(self) -> int:
        """ゲームの進行状態を取得
        :return int :0: 取得失敗 1:待機中, 2:対戦中, 3:大戦終了
        """
        url_get_room = self._URL + "/rooms/" + str(self._room_id)
        result = self._session.get(url_get_room)
        result.raise_for_status()
        return result.json()["state"]


def get_empty(start=8000):
    URL = "https://damp-earth-70561.herokuapp.com"
    url_get_all_rooms = URL + "/rooms/"
    session = requests.Session()
    result = session.get(url_get_all_rooms)
    result.raise_for_status()
    rooms = [i["id"] for i in result.json()]
    num = start
    while True:
        num += 1
        if num not in rooms:
            return num
