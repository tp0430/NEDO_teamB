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


class APICom:
    """通信用モジュール

    :param str player_id: プレーヤーID
    :param str player_name: プレーヤー名
    :param int room_id: ルームID
    """

    def __init__(self, player_name, room_id):

        self._URL = "https://damp-earth-70561.herokuapp.com"
        self._session = requests.Session()
        self._HEADERS = {"Content-Type": "application/json"}

        self._player_list = self._register_player()

        self._player_name = player_name
        self._player_id = self._player_list[player_name]
        self._room_id = room_id  # ここの値は2000~2999の範囲(使ってもいい部分)で都度変える。

    def _register_player():
        ret = {}
        ret["B"] = "7d025351-7836-4904-a48f-f58019b6ca77"
        ret["B2"] = "a9c2784a-2279-4215-bc7d-1255dbdf911d"

        return ret


    def get_rooms(self):
        """全ての対戦部屋の情報を取得する.
        :return:
        """
        url_get_all_rooms = self._URL + "/rooms/"

        result = self._session.get(url_get_all_rooms)

        # print(result.status_code)
        return result.json()

    def enter_room(self):
        """対戦部屋を作成し、指定したユーザを登録する。
        待機中の状態の対戦部屋が存在する場合は、指定したユーザを該当の対戦部屋のプレイヤーとして登録する。
        selfにルームIDを指定した場合は、該当のルームIDの対戦部屋にユーザを登録。

        :return:
        """
        url_enter_room = self._URL + "/rooms/"
        enter_room_json = {"player_id": self._player_id, "room_id": self._room_id}

        result = self._session.post(
            url_enter_room, headers=self._HEADERS, json=enter_room_json
        )

        # print(result.status_code)
        return result.json()

    def get_room(self):
        """指定した対戦部屋の情報を取得する
        :return:
        """
        url_get_room = self._URL + "/rooms/" + str(self._room_id)

        result = self._session.get(url_get_room)

        # print(result.status_code)
        return result.json()

    def get_table(self):
        """対戦情報テーブル(現在のターン, hit&blowの履歴, 勝敗の判定)を取得する.
        :return:
        """
        url_get_table = self._URL + "/rooms/" + str(self._room_id) + "/players/" + self._player_name + "/table"

        result = self._session.get(url_get_table)

        # print(result.status_code)
        return result.json()


    def post_hidden(self, hidden_number : str):
        """相手が当てる5桁の16進数を登録する. ※アルファベットは小文字のみ
        :return:
        """
        url_post_hidden = self._URL + "/rooms/" + str(self._room_id) + "/players/" + self._player_name + "/hidden"
        post_hidden_json = {"player_id": self._player_id, "hidden_number": hidden_number}

        result = self._session.post(url_post_hidden, headers=self._HEADERS, json=post_hidden_json)

        # print(result.status_code)
        return result.json()

    def post_guess(self, guess_number : str):
        """推測した数字を登録する
        :return:
        """
        url_post_guess = self._URL + "/rooms/" + str(self._room_id) + "/players/" + self._player_name + "/table/guesses"
        post_guess_json = {"player_id": self._player_id, "guess": guess_number}

        result = self._session.post(url_post_guess, headers=self._HEADERS, json=post_guess_json)

        # print(result.status_code)
        return result.json()

    def get_game_state(self) -> int:
        """ゲームの進行状態を取得
        :return int :0: 取得失敗 1:待機中, 2:対戦中, 3:大戦終了
        """
        url_get_room = self._URL + "/rooms/" + str(self._room_id)
        result = self._session.get(url_get_room)

        if result.status_code == 200:
            return result.json()["state"]
        else:
            return 0