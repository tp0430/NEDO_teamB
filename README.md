# NEDO_teamB

NEDOプログラミング課題のチームBです

## 環境

- python == 3.9.1

## セットアップ方法

```sh
pyenv install 3.9.1
pyenv local 3.9.1
pyenv rehash
pipenv install --dev --python 3.9.1
pipenv shell
```

## 実行方法

GUIを用いた通常プレイの場合

```sh
python hit_and_blow\hit_and_blow.py
```

最初のルームidを指定し、100回連続で対戦する場合

```sh
python hit_and_blow\hit_and_blow_auto.py
```
