import requests
import json
import re
API_URL = 'https://api-inference.huggingface.co/models/bigscience/bloom'
TOKEN = open('copy-bloom/.env').read().strip()
MAX_SEQUENCE_LENGTH = 411 # actually 511 but leaving 100 words for final point
def create_outline(topic:str, n_points:int=3):
    points = []
    text = f"the following are {str(n_points)} of our outline points in an article about '{topic}': \n 1: "
    for i in range(n_points):
        point_split = []
        query_text = text
        while len(point_split) < 2:
            query_text = query(query_text)
            point = query_text[len(text):]
            point_split = re.split(r'[\n]',point)
        points.append(point_split[0])
        if len(point_split[0].split(' ')) + len(text.split(' ')) + 2 < MAX_SEQUENCE_LENGTH:
            text += point_split[0]
            text += f"\n{i+2}: "
            print(text,  end='\n====================\n')
    return points

def query(payload):
    headers = {"Authorization": TOKEN}
    data = {
        "inputs": payload,
        "parameters": {
            "top_k": 10,
            "top_p": 0.9,
            "do_sample": True,
        },
        "options": {
            "use_gpu": True,
            "use_cache": False,
        }
    }
    response = requests.post(API_URL,headers=headers,data=json.dumps(data))
    return response.json()[0]['generated_text']


if __name__ == '__main__':
    points = create_outline('artificial intelligence', 3)
    for point in points:
        print(point, end='\n\n')