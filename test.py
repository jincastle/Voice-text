
a = "이 차의 가격은?"
b = "신차 가격은 뭐야?"

def test():
    allowed_values={492}
    labs_danji_no='492'
    # if labs_danji_no not in ['492', '777']:
    #     labs_danji_no = '999'
    body = {
        "car_seq": 1,
        "video_id": 1,
        "video_url": 1
    }
    if labs_danji_no is not None:
        body["labs_danji_no"] = labs_danji_no
    print(body)

if __name__ == "__main__":
    test()