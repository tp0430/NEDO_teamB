# NEDO_teamB

NEDOプログラミング課題のチームBです

## 環境

- python == 3.9.1

## セットアップ方法

streamlitと関連ライブラリが多いらしく初回は時間がかかるかも。

```sh
pyenv install 3.9.1
pyenv local 3.9.1
pyenv rehash
pipenv install --dev --python 3.9.1
pipenv shell
```

## 実行方法

初回はメールアドレスの入力を求められるが空欄でもOK。  
実行するとブラウザが開き文字が表示されるはず。  
終了するときは`Ctrl+C`で終了する。  

```sh
streamlit run hit_and_blow.py
```
