import os
import json

import gtts as gtts
import requests

# /main.py
from fastapi import FastAPI, File, Request
from gtts import gTTS
import datetime
from fastapi.middleware.cors import CORSMiddleware
import openai
import boto3
from config import settings


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client_id = settings.client_id
client_secret = settings.client_secret
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
openai.api_key = settings.api_key



# 실행 명령어 uvicorn main:app --reload
@app.post("/")
async def root():
    lang = "Kor"  # 언어 코드 ( Kor )
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
    data = open('voicefile/testfile.mp3', 'rb')
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(url, data=data, headers=headers)
    rescode = response.status_code
    if (rescode == 200):
        return {'result': response.text}
    else:
        return {"Error": response.text}

@app.post("/voice")
async def root(file: bytes = File(...)):
    lang = "Kor"  # 언어 코드 ( Kor )
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
    data = file
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(url, data=data, headers=headers)
    rescode = response.status_code
    if (rescode == 200):
        cwd = os.getcwd()
        file_name = "result.txt"
        result = json.loads(response.text)
        question = result['text']
        with open(os.path.join(cwd, file_name), "w", encoding="utf-8") as f:
            f.write(question)
        prompt = f"질문: {question}\n답변: "
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response.choices[0].text.strip()
        print(answer)
        return {'result': answer}
    else:
        return {"Error": response.text}

@app.post("/question")
async def root(request: Request):
    question = await request.json()
    print(question['question'])
    prompt = f"질문: {question['question']}\n답변: "
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    print(answer)
    return {'result': answer}

# 영어 질문 한글 답변
@app.post("/voice2")
async def root(file: bytes = File(...)):
    lang = "Kor"  # 언어 코드 (Kor)
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
    data = file
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(url, data=data, headers=headers)
    rescode = response.status_code
    if (rescode == 200):
        cwd = os.getcwd()
        file_name = "result.txt"
        result = json.loads(response.text)
        question = result['text']

        keywords = ["가격", "성능", "비슷한 차량"]

        for keyword in keywords:
            if keyword in question:
                if keyword == "가격":
                    message = "신차 가격이 얼마예요?"
                elif keyword == "성능":
                    message = "이차의 성능리스트를 알려주세요."
                elif keyword == "비슷한 차량":
                    message = "어떤 차량이 비슷한 차량이에요?"
                print(message)

        # 번역
        client = boto3.client('translate', region_name='us-west-2')
        response = client.translate_text(Text=question, SourceLanguageCode="ko", TargetLanguageCode="en")
        question_en = response.get('TranslatedText')

        with open(os.path.join(cwd, file_name), "w", encoding="utf-8") as f:
            f.write(question)
        prompt = f"Question: {question_en}\nAnswer: "
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response.choices[0].text.strip()

        # 번역
        response = client.translate_text(Text=answer, SourceLanguageCode="en", TargetLanguageCode="ko")
        answer_ko = response.get('TranslatedText')

        print(answer_ko)
        return {'result': answer_ko}
    else:
        return {"Error": response.text}

@app.post("/text")
async def root(text):
    question = text
    prompt = f"질문: {question}\n답변: "
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    print(answer)
    return {'result': answer}


@app.post("/voice1")
async def root():

    with open("result.txt", "r") as f:
        text = f.read()

    tts=gTTS(text=text, lang='ko')
    tts.save(f"result_{current_time}.mp3")


@app.get("/find_text")
async def root():
    with open("result.txt", "r") as f:
        text = f.read()








