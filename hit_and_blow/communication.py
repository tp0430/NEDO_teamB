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
    :param str URL:サーバのURL
    :param requests.sessions.Session session: session id
    :param str player_id: プレーヤーID
    :param dict HEADERS: ヘッダ
    :param str player_name: プレーヤー名
    :param int room_id: ルームID
    """

    def __init__(self, player_id:str, player_name:str, room_id:str):
        """
        :param str player_id:プレイヤーID
        :param str player_name:プレイヤー名
        :param str room_id:ルームID
        :rtype:None
        :return:なし
        """
        self.URL = "https://damp-earth-70561.herokuapp.com"
        self.session = requests.Session()
        self.player_id = player_id
        self.HEADERS = {"Content-Type": "application/json"}
        self.player_name = player_name

        self.room_id = room_id  # ここの値は2000~2999の範囲(使ってもいい部分)で都度変える。

    def get_rooms(self)->dict:
        """全ての対戦部屋の情報を取得する.
        :rtype:dict
        :return: 全ての対戦部屋のURL
        """
        url_get_all_rooms = self.URL + "/rooms/"

        result = self.session.get(url_get_all_rooms)

        # print(result.status_code)
        return result.json()

    def enter_room(self)->dict:
        """対戦部屋を作成し、指定したユーザを登録する。
        待機中の状態の対戦部屋が存在する場合は、指定したユーザを該当の対戦部屋のプレイヤーとして登録する。
        selfにルームIDを指定した場合は、該当のルームIDの対戦部屋にユーザを登録。

        :rtype:dict
        :return:
        """
        url_enter_room = self.URL + "/rooms/"
        enter_room_json = {"player_id": self.player_id, "room_id": self.room_id}

        result = self.session.post(
            url_enter_room, headers=self.HEADERS, json=enter_room_json
        )

        # print(result.status_code)
        return result.json()

    def get_room(self)->dict:
        """指定した対戦部屋の情報を取得する

        :rtype:dict
        :return: 指定した対戦部屋のURL
        """
        url_get_room = self.URL + "/rooms/" + str(self.room_id)

        result = self.session.get(url_get_room)

        # print(result.status_code)
        return result.json()

    def get_table(self)->dict:
        """対戦情報テーブル(現在のターン, hit&blowの履歴, 勝敗の判定)を取得する.

        :rtype:dict
        :return: 現在のターン，hit&blowの履歴，勝敗の判定
        """
        url_get_table = self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.player_name + "/table"

        result = self.session.get(url_get_table)

        # print(result.status_code)
        return result.json()


    def post_hidden(self, hidden_number : str)->dict:
        """相手が当てる5桁の16進数を登録する. ※アルファベットは小文字のみ

        :param str hidden_number: こちらが指定する答え
        :rtype:dict
        :return:{"プレイヤーID":"指定した答え"}
        """
        url_post_hidden = self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.player_name + "/hidden"
        post_hidden_json = {"player_id": self.player_id, "hidden_number": hidden_number}

        result = self.session.post(url_post_hidden, headers=self.HEADERS, json=post_hidden_json)

        # print(result.status_code)
        return result.json()

    def post_guess(self, guess_number : str)->dict:
        """推測した数字を登録する
        :param str guess_number: 推測した数値
        :rtype:dict
        :return:{"プレイヤーID":"推測した答え"}
        """
        url_post_guess = self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.player_name + "/table/guesses"
        post_guess_json = {"player_id": self.player_id, "guess": guess_number}

        result = self.session.post(url_post_guess, headers=self.HEADERS, json=post_guess_json)

        # print(result.status_code)
        return result.json()
