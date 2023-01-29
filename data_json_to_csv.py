import glob
import json
import pandas as pd

def get_category_index(domain_name):
    if domain_name == "토크쇼" or "강의/강연" or "건강/의학" or "경제시사" or "교양" or "교육/문화예술" or "도서/교양" or "퀴즈/게임": return "T"
    elif domain_name == "반려동물" or "생활정보" or "스포츠" or "시사평론" or "예술/문화" or "음악평론" or "정보/토크" or "정치/경제" or "취미": return "T"
    elif domain_name == "토론/대담" or "푸드/요리": return "T"
    elif domain_name == "드라마/영화": return "D"
    elif domain_name == "버라이어티쇼/예능": return "V"
    elif domain_name == "뉴스": return "N"

def convert_demographic_map(speaker):
    id, age, sex = speaker["id"], speaker["age"], speaker["sex"]
    return {"id": id, "age": age.split("대")[0], "sex": sex}

def convert_data_frame(category, demograpic_dictionary, utterance):
    speaker = demograpic_dictionary[utterance["speaker_id"]]
    return {"input": utterance["original_form"], "category": category, "age": speaker["age"], "sex": speaker["sex"]}

dirs = './sample_data'

def get_only_json_file(file_name):
    return "json" in file_name

files = filter(get_only_json_file, glob.glob(dirs + '/**', recursive=True))
file_count = 0
data_frame = []
for file_name in files:
    with open(file_name, "r") as f:
        data = json.load(f)
        demograpic_dictionary = {}
        for speaker in map(convert_demographic_map, data["speaker"]): 
            demograpic_dictionary[speaker["id"]] = speaker
        category = get_category_index(data["metadata"]["domain"])
        for utterance in data["utterance"]:  
            if utterance["speaker_id"] in demograpic_dictionary.keys():
                data_frame.append(
                    convert_data_frame(category, demograpic_dictionary, utterance)
                )
        file_count += 1
        print("file_count: ", file_count)
df = pd.read_json(json.dumps(data_frame))
df.to_csv('data_frame.csv')