import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["GPT_API_KEY"]
openai.api_key = api_key

asked = (" When you recommend clothes, recommend tops, bottoms, hats, outerwear, and shoes. "
         "Also, define each in one word only. For example, tshirts, jeans, cap.. ")

# Create ChatGPT Answer
response = openai.ChatCompletion.create(
    model="ft:gpt-3.5-turbo-0125:personal:test01:95Q5lRy9",     # fine-tuning model's name
    messages=[
        {"role": "system", "content": "a delicate clothes coordinator who recommends clothes according to the weather"},
        {"role": "user", "content": "Please recommend clothes to wear on broken clouds days in -10 degrees"}
    ]
)

# 응답 출력
print(response)
print("=============")
print(response.choices[0].message.content)
