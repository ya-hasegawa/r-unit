import os

from flask import Flask, jsonify, request, abort
from google.cloud import bigquery

# ==================================================
# インスタンスを生成
# ==================================================
app = Flask(__name__)          # Flaskクラスから生成したオブジェクト（インスタンス）
app.json.ensure_ascii = False  # 日本語の文字化け対応


# ==================================================
# ルーティングを定義
# ==================================================
# ルーティングとは、「URL」と「処理」を紐づけること
# Flaskのルーティングでは、「URL」と「関数」を紐づける
# URL /api/v1/hello にGETメソッドでアクセスがあった場合、直後の関数 hello() で処理することを指定（紐づけ）

@app.route('/api/v1/hello', methods=['GET'])
def hello():
    # 環境変数からプロジェクト名、データセット名、テーブル名を取得
    project_id = os.environ.get('PROJECT_ID')
    dataset_id = os.environ.get('DATASET_ID')
    table_id = os.environ.get('TABLE_ID')

    # 認証情報のチェック
    auth_header = request.headers.get('Authorization')
    # 値が存在しない or 値が Bearer: hogehoge ではない
    if not auth_header or auth_header != 'Bearer: hogehoge':
        abort(403)

    # # サービスアカウントの認証（ローカルPCでの検証用）
    # key_path = 'credentials.json'
    # # サービスアカウントキーのパスを環境変数に設定
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

    # BigQueryクライアントオブジェクトの作成
    client = bigquery.Client()
    # client = bigquery.Client(project=project_id)

    # SQLの実行
    query = f"""
        SELECT weather FROM `{project_id}.{dataset_id}.{table_id}` LIMIT 1
    """
    query_job = client.query(query)
    results = query_job.result()  # ジョブが完了するまで待機

    # 結果を返す
    for row in results:
        return jsonify({'text': row.weather})  # jsonify：JSON 形式で返す


# ==================================================
# FlaskのWebサーバを起動
# ==================================================
# このプログラムが直接実行されたかどうかを判定。直接実行された場合、「__name__」は「__main__」という値になる
if __name__ == '__main__':
    # デフォルトは、debug=False、host="127.0.0.1"(自分のPC)、port=5000
    # 127.0.0.1：自分のPCからのみアクセス可能、0.0.0.0：外部からアクセス可能
    # app.run(debug=True)
    app.run(debug=True, host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)))