# coding: UTF-8
"""
    * File name: hit_and_blow.py
    * Description: hit and blowのmainモジュール
    * Created on: September 22
    * Created by: KENTA Mizuhara
"""


import tkinter as tk
import tkinter.ttk as ttk

from sys import api_version
from display import DispLogin
from display import DispWaiting
from display import Game




def main():
    Game.init()

    disp_login = DispLogin()
    disp_login.show()

    Game.root.mainloop()


if __name__ == "__main__":

    main()
