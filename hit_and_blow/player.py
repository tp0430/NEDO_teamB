
import time

from communication import APICom
from brain import Brain


def start_game(room_id = None, player_id = None, player_name = None):
    
    #各種パラメータを設定
    if player_id == None:
        player_id = input("enter player id : ")
    if player_name == None:
        player_name = input("enter player name : ")
    if room_id == None:
        room_id = int(input("enter room id : "))
    hidden_number = input("enter hidden number : ")

    # 通信モジュールを生成
    api_com = APICom(player_id= player_id, player_name= player_name, room_id= room_id)

    # 自動対戦用のbrainを生成
    brain = Brain()

    # 入室
    result_enter_room = api_com.enter_room()

    # 相手が来るまで待機
    while api_com.get_room()["state"] == 1:
        print("now waiting opponent")
        time.sleep(5)

    # ゲーム開始, 自分の数字を登録
    api_com.post_hidden(hidden_number= hidden_number)

    # 相手が数字を登録するまで待機
    while api_com.get_table()["now_player"] == None:
        print("now waiting opponent to regist hidden number")
        time.sleep(1)

    # ゲーム進行中
    print("GAME START!")
    guess_num = None
    guess_result = None
    while api_com.get_table()["state"] == 2:

        table = api_com.get_table()
        if table["now_player"] == player_name:

            guess_num = brain.guess(guess_num, guess_result)
            api_com.post_guess(guess_number= guess_num)
            latest_result = api_com.get_table()["table"][-1]
            guess_result = (latest_result["hit"], latest_result["blow"])

            print("{} : {}".format(guess_num, guess_result))

            time.sleep(1)

    if api_com.get_table()["winner"] == player_name:
        print("YOU WIN!")
    else:
        print("YOU LOSE")

if __name__ == "__main__":
    start_game()