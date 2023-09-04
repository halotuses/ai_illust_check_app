import numpy as np
import cv2
import os
from scipy.stats import entropy
from sklearn.linear_model import LogisticRegression
from PIL import Image

# ロジスティック回帰モデルの初期化
model = LogisticRegression()
# モデルの係数・切片の設定
model.coef_ = np.array([[-0.0140, 0.9935, 0.0169, -1.7621, -0.0126, 0.5156]])
model.intercept_ = np.array([2.7925])
model.classes_ = np.array([0, 1]) 

#画像から特徴量を抽出する関数
def extract_features(image: Image.Image):

    # PILのImageをNumPy配列に変換
    image_np = np.array(image)

    # OpenCVはBGRフォーマットを使用するため、RGBからBGRに変換
    image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    features = []

    # 特徴量を計算
    for channel in [2, 1, 0]:  # 2: red, 1: green, 0: blue
        channel_data = image[:, :, channel].ravel()
        mean = np.mean(channel_data)
        hist = np.bincount(channel_data, minlength=256)
        ent = entropy(hist)
        features.extend([mean, ent])

    return features

#特徴量からAI確率を予測する関数
def predict_image_probabilities(model, image: Image.Image):
    features = extract_features(image)
    features_reshaped = np.array(features).reshape(1, -1)
    probabilities = model.predict_proba(features_reshaped)
    return probabilities


#テスト用
if __name__ == '__main__':
    results_proba = {}

    # 'investigation' フォルダの画像を読み込む
    for image_file in os.listdir('investigation'):
        # 拡張子の制限
        if not image_file.endswith(('.png', '.jpg', '.jpeg', '.JPG', '.PNG')):
            continue
        image_path = os.path.join('investigation', image_file)

        # PILで画像を読み込み、RGBに変換
        image = Image.open(image_path).convert('RGB')
        proba = predict_image_probabilities(model, image)

        results_proba[image_file] = proba

    #結果の表示
    for image_file, proba in results_proba.items():
        print(f"{image_file}: AIの確率 = {proba[0][1]*100:.2f}%, Humanの確率 = {proba[0][0]*100:.2f}%")
