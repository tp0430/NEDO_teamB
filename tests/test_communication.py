# coding: UTF-8
"""
    * File name: test_communication.py
    * Description: communication.pyの基本的なAPI利用についてテストする。
    * Created on: September 27
    * Created by: KENTA Mizuhara
"""
import requests

from hit_and_blow.communication import APICom


#room_idは毎回変える。
room_id = 8000
url_get_all_rooms = "https://damp-earth-70561.herokuapp.com/rooms"
session = requests.Session()
all_rooms = session.get(url_get_all_rooms)
all_used_id = [js["id"] for js in all_rooms.json()]
while room_id in all_used_id:
    room_id += 1

com_b = APICom(
    player_id="7d025351-7836-4904-a48f-f58019b6ca77", player_name="B", room_id=room_id,
)
com_b2 = APICom(
    player_id="a9c2784a-2279-4215-bc7d-1255dbdf911d", player_name="B2", room_id=room_id,
)



def test_get_room():
    # 部屋の取得
    com_b.enter_room()
    get_b = com_b.get_room()

    assert (
        get_b["id"] == room_id
        and get_b["player1"] == "B"
        and get_b["player2"] == None
    )


def test_get_room2():
    com_b2.enter_room()
    get_b2 = com_b2.get_room()
    assert (
        get_b2["id"] == room_id
        and get_b2["player1"] == "B"
        and get_b2["player2"] == "B2"
    )

def test_post_hidden():
    # 5桁の数字の登録
    com_b.post_hidden("abc12")
    com_b2.post_hidden("98fa4")
    assert True

def test_post_guess1():
    # 推測した数字を登録。Bから
    com_b.post_guess("34f12")
    get_tab_b = com_b.get_table()
    assert get_tab_b["table"][0]["guess"] == "34f12"

def test_post_guess2():
    # B2が推測した数字を登録
    com_b2.post_guess("4e25a")
    get_tab_b2 = com_b2.get_table()
    assert get_tab_b2["table"][0]["guess"] == "4e25a"

def test_post_guess3():
    # Bが勝利
    com_b.post_guess("98fa4")
    com_b2.post_guess("24198")
    get_tab_b = com_b.get_table()
    assert get_tab_b["winner"] == "B"

