
import sys

from player import Player

ANS_LEN: int = 5
MIN_ANS: int = 0
MAX_ANS: int = 15
REPEAT_NUM: int = 100
PLAYER_NAME: str = "B"
FIRST_ROOM_ID: int = 1  # 上野さん、対戦時に設定してください。


def main(first_room_id = FIRST_ROOM_ID, repeat = REPEAT_NUM):
    for i in range(repeat):
        player = Player(room_id= first_room_id + i,mode= 1, player_name= PLAYER_NAME)
        player.play_game_internal()

if __name__ == "__main__":

    main(first_room_id= int(sys.argv[1]))
