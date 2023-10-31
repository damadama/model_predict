# import pickle
# import pandas as pd
# from pathlib import Path

# # pklファイルのパスの指定
# path = Path(__file__).resolve().parent

# # モデルをPickleファイルから読み込む
# with open(path.joinpath('model.pkl'), 'rb') as model_file:
#     model = pickle.load(model_file)

# # 空のデータフレームを作成
# df = pd.DataFrame(columns=["suction_cup_diameter", "plate_thickness", "weight", "vacuum_pressure"])

# plate_thickness = 0.6
# weight = 20
# suction_cup_diameter = list(range(40, 81, 10))
# vacuum_pressure = list(range(25, 101, 5))

# # データフレームを構築
# dataframes_to_concat = []

# for suction_cup_diameter_values in suction_cup_diameter:
#     temp_df = pd.DataFrame({
#         "suction_cup_diameter": [suction_cup_diameter_values] * len(vacuum_pressure),
#         "plate_thickness": [plate_thickness] * len(vacuum_pressure),
#         "weight": [weight] * len(vacuum_pressure),
#         "vacuum_pressure": vacuum_pressure
#     })
#     dataframes_to_concat.append(temp_df)

# # pd.concat() を使用してデータを結合
# df = pd.concat(dataframes_to_concat, ignore_index=True)

# # 予測結果を格納する新しい列を作成
# df['predictions'] = None

# # 各行の特徴量をモデルに渡して予測
# for index, row in df.iterrows():
#     features = row[['suction_cup_diameter', 'plate_thickness', 'weight', 'vacuum_pressure']].values.reshape(1, -1)
#     prediction = model.predict(features)
#     df.at[index, 'predictions'] = prediction[0]

# # データフレームをCSVファイルとして保存
# # df.to_csv("output.csv",index=False)

# # データフレームの表示
# # print(df)



import pickle
import PySimpleGUI as sg
import pandas as pd
# from pathlib import Path
import os

# スクリプトが存在するディレクトリの絶対パスを取得
script_directory = os.path.dirname(os.path.abspath(__file__))
model_file_path = os.path.join(script_directory, 'model.pkl')
# モデルをPickleファイルから読み込む
with open(model_file_path, 'rb') as model_file:
    model = pickle.load(model_file)

# PySimpleGUIのウィンドウレイアウト
layout = [
    [sg.Text("重さ(9~20kg):"), sg.InputText(key="weight")],
    [sg.Text("板厚(0.55 or 0.6mm):"), sg.InputText(key="plate_thickness")],
    [sg.Button("計算開始")]
]

# データフレームを構築
dataframes_to_concat = []
# 吸着カップ径と真空圧力の設定値
suction_cup_diameter = list(range(40, 81, 10))
vacuum_pressure = list(range(25, 101, 5))

# ウィンドウの作成
window = sg.Window("Model Prediction", layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == "計算開始":
        # 入力値を取得
        weight = float(values["weight"])
        plate_thickness = float(values["plate_thickness"])

        # 入力値をDataFrameに変換
        for suction_cup_diameter_values in suction_cup_diameter:
            temp_df = pd.DataFrame({
                "suction_cup_diameter": [suction_cup_diameter_values] * len(vacuum_pressure),
                "plate_thickness": [plate_thickness] * len(vacuum_pressure),
                "weight": [weight] * len(vacuum_pressure),
                "vacuum_pressure": vacuum_pressure
            })
            dataframes_to_concat.append(temp_df)

        # pd.concat() を使用してデータを結合
        df = pd.concat(dataframes_to_concat, ignore_index=True)

        # 予測結果を格納する新しい列を作成
        df['predictions'] = None

        # 各行の特徴量をモデルに渡して予測
        for index, row in df.iterrows():
            features = row[['suction_cup_diameter', 'plate_thickness', 'weight', 'vacuum_pressure']].values.reshape(1, -1)
            prediction = model.predict(features)
            df.at[index, 'predictions'] = prediction[0]

        # predictions==0(=歪無)のみ抽出
        df_non_distorted = df[df['predictions'] == 0]
        # データフレームをCSVファイルとして保存
        df.to_csv("output_raw.csv",index=False)
        df_non_distorted.to_csv("output_non_distorted.csv",index=False)

        # 予測結果を表示
        sg.popup(f"計算結果を出力しました")

window.close()
# test















