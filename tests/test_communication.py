# coding: UTF-8
"""
    * File name: test_communication.py
    * Description: communication.pyの基本的なAPI利用についてテストする。
    * Created on: September 27
    * Created by: KENTA Mizuhara
"""

from hit_and_blow.communication import APICom

ROOM_ID = 8001


def test_APICom():
    ComB = APICom(
        player_id="7d025351-7836-4904-a48f-f58019b6ca77",
        player_name="B",
        room_id=ROOM_ID,
    )
    ComB2 = APICom(
        player_id="a9c2784a-2279-4215-bc7d-1255dbdf911d",
        player_name="B2",
        room_id=ROOM_ID,
    )

    # 入室
    enter_B = ComB.enter_room()
    enter_B2 = ComB2.enter_room()
    assert enter_B["id"] == ROOM_ID and enter_B["player1"] == "B"
    assert enter_B2["id"] == ROOM_ID and enter_B2["player2"] == "B2"

    # 部屋の取得
    get_B = ComB.get_room()
    get_B2 = ComB2.get_room()
    assert (
        get_B["id"] == ROOM_ID
        and get_B["player1"] == "B"
        and get_B["player2"] == "B2"
        and get_B["state"] == 2
    )
    assert (
        get_B2["id"] == ROOM_ID
        and get_B2["player1"] == "B"
        and get_B2["player2"] == "B2"
        and get_B2["state"] == 2
    )

    # 5桁の数字の登録
    hidden_B = ComB.post_hidden("abc12")
    hidden_B2 = ComB2.post_hidden("98fa4")
    assert hidden_B["selecting"] == True
    assert hidden_B2["selecting"] == False

    # 推測した数字を登録。Bから
    ComB.post_guess("34f12")
    get_tab_B = ComB.get_table()
    assert get_tab_B["table"][0]["guess"] == "34f12"

    # B2が推測した数字を登録
    ComB2.post_guess("4e25a")
    get_tab_B2 = ComB2.get_table()
    assert get_tab_B2["table"][0]["guess"] == "4e25a"

    # Bが勝利
    ComB.post_guess("98fa4")
    ComB2.post_guess("24198")
    get_tab_B = ComB.get_table()
    assert get_tab_B["winner"] == "B"

