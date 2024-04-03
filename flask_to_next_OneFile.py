import os
from flask import Flask, request, jsonify
import requests
import time
from dotenv import load_dotenv
from flask_cors import CORS
from openAi_server import ai_server
import json
import classification_OneFile as onefile

app = Flask(__name__)
CORS(app, supports_credentials=True)
load_dotenv()

# 전송할 스프링 서버 주소값
spring_server_url = os.getenv("SPRING_SERVER_URL")

@app.route('/closet/styleai', methods=['POST'])
def handle_request():
    if request.method == 'POST':

        start_time = time.time()

        data = request.form.to_dict()

        resDict = {}

        print("data > ", data)

        for key, value in data.items():
            img_url, style, score = onefile.predict_cloth(key, value)
            resDict[style] = score

        print(resDict)

        # 서버에 보내기
        try:
            end_time = time.time()
            print(f"Total execution time: {end_time - start_time}")

            return resDict
        except Exception as e:
            print("Error while sending data to Spring server:", str(e))
            return 'Error while sending data to Spring server!'

@app.route('/recommend/cloth', methods=['POST'])
def handled_clothesAi():
    if request.method == 'POST':
        accessToken = request.headers["Authorization"]      # jwt 토큰
        cloth_list = request.json

        # openai 응답 메시지
        response = ai_server(cloth_list)
        params = {"response" : response}
        print(response)

        try:
            headers = {'Authorization': accessToken}       # jwt 토큰 헤더 설정
            message = requests.get(spring_server_url, params=params, headers=headers)
            if message.status_code == 200:
                data = json.loads(message.text)
                print(data)
                # print("data > ", data)
                # for d in data:
                #     print("d > ", json.dumps(d))

                return jsonify({"message" : data})
            else:
                print("rrr >" , message.text)
                return jsonify({"message" : "send fail"})
        except requests.exceptions.RequestException as e:
            return jsonify({'error': 'Failed to send data: ' + str(e)})


if __name__ == '__main__':
    app.run(host=os.getenv("HOST_IP"), port=os.getenv("PORT"), debug=True)
