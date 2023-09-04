
from flask import Flask, request, jsonify, render_template
from PIL import Image
import io
from RGBjudgment import model, predict_image_probabilities
from flask_cors import CORS
import logging

# Flaskアプリの初期化・設定
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG) 
CORS(app) 

# ファイル拡張子指定
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# ファイル拡張子を確認する
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ホームページを表示するルート
@app.route('/')
def index():
    return render_template('index.html')

# 画像に対する予測を行うルート
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # リクエスト情報のログ出力
        app.logger.info("Received a request to /predict endpoint.")
        app.logger.info("Headers: %s", request.headers)
        app.logger.info("Body: %s", request.data[:100])  

        # 送信されたファイルを取得
        uploaded_file = request.files.get('image')
        if not uploaded_file:
            return jsonify({"error": "No image uploaded"}), 400

        # ファイル拡張子の確認
        if not allowed_file(uploaded_file.filename):
            return jsonify({"error": "Invalid file extension. Please upload a JPG or PNG image."}), 400

        # Pillowで送信された画像を開く
        image = Image.open(io.BytesIO(uploaded_file.read()))

        # アルファチャンネルを削除してRGB形式に変換
        image = image.convert("RGB")

        # モデルで画像に対する予測を行う
        proba = predict_image_probabilities(model, image)

        # 予測結果をレスポンスとして格納
        response_data = {
            "AI_probability": int(float(proba[0][1] * 100)),
            "Human_probability": int(float(proba[0][0] * 100))
        }

        app.logger.info(f"Response data: {response_data}")

        return jsonify(response_data)

    except Exception as e:
        # エラーが発生した場合のログ出力とエラーレスポンス
        app.logger.error(f"Error occurred during prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 予期しないエラーをキャッチするためのエラーハンドラ
@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"Unexpected error occurred: {str(e)}")
    return jsonify({"error": "Unexpected error occurred"}), 500

# スクリプトとして実行された場合の処理
if __name__ == '__main__':
    app.run(debug=True)
