# Pythonイメージをベースにする
FROM python:3.8

# /appディレクトリを作成し、作業ディレクトリとして設定
WORKDIR /app

# requirements.txtをコピーし、依存関係をインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# Flaskアプリケーションを起動
CMD ["flask", "--app", "main.py", "run", "--host=0.0.0.0", "--port=5000"]