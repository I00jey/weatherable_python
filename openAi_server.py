import openai
import os
from dotenv import load_dotenv

def ai_server(cloth_list):
    load_dotenv()

    api_key = os.environ["GPT_API_KEY"]
    gpt_model = os.environ["GPT_MODEL_NAME"]
    openai.api_key = api_key

    # load your cloth list
    after_asked = "나는 아래의 옷들을 갖고 있어.\n"
    for major_category in cloth_list:
        if major_category != "weather":
            after_asked += f"{major_category} : "
            for item in cloth_list[major_category]:
                after_asked += f"{item[0]} --{item[1]}--, "
            after_asked += "\n"

    before_asked = ("상의, 하의, 아우터, 신발, 모자로 나누어서 각 종류 당 1개의 아이템을 내가 가진 옷을 기반으로 추천해줘. 또한 너는 몇가지 출력 수칙을 지켜야한다."
                    "1. 옷의 중분류(맨투맨, 니트, 부츠, 패딩 등)을 확인하고 이름만을 한줄에 하나씩 출력해야한다."
                    "2. 추천 양식은 부위 : 이름으로만 출력해야한다. 즉, -- 뒤 문자열은 출력하지마라.sunny"
                    "3. 만약 해당 부위에 아이템이 없다면 부위 : 없음 으로 해라."
                    )

    # ChatGPT API를 사용하여 대화 생성
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": "옷 코디네이터"},
            {"role": "user", "content": after_asked + f"기온 : {cloth_list['weather'][0]}도, 날씨 : {cloth_list['weather'][1]} / 이러한 조건일 때 보유한 옷의 종류를 보고 옷을 추천해줘 \n" + before_asked}
        ]
    )

    # 응답 출력
    print(response)
    print("=============")
    return response.choices[0].message.content
