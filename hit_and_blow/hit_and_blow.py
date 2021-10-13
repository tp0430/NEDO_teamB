# coding: UTF-8
"""
    * File name: hit_and_blow.py
    * Description: hit and blowのmainモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

from display import Game
from display import on_closing
import logging
from logging import getLogger, StreamHandler, Formatter

logger = getLogger("hit_and_blow")
stream_handler = StreamHandler()
logger.setLevel(logging.CRITICAL)
# ログ出力フォーマット設定
handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)



def main():
    Game.init()
    Game.root.protocol("WM_DELETE_WINDOW", on_closing)
    Game.root.mainloop()


if __name__ == "__main__":
    main()
