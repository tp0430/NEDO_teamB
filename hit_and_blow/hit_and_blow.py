# coding: UTF-8
"""
    * File name: hit_and_blow.py
    * Description: hit and blowのmainモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""

from display import Game
from display import on_closing


def main():
    Game.init()
    Game.root.protocol("WM_DELETE_WINDOW", on_closing)
    Game.root.mainloop()


if __name__ == "__main__":
    main()
