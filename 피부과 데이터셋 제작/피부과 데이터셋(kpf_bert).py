import json
import re
import os
import csv

base_path = os.getcwd() 
folder_path = os.path.join(base_path, "피부과 데이터셋 제작")
output_file = os.path.join(base_path, "result.csv")

def fast_triple_extractor(json_data):
    """JSON 데이터에서 Head, Relation, Tail을 추출하는 함수"""
    # 데이터가 리스트 형태일 경우를 대비한 안전장치
    if isinstance(json_data, list):
        json_data = json_data[0] if len(json_data) > 0 else {}

    question = json_data.get("question", "")
    answer = json_data.get("answer", "")
    
    if not question or not answer:
        return []

    # 정답(Head) 정제
    head = re.sub(r'^[0-9]+\)\s*', '', str(answer)).split(' (')[0].strip()
    
    words = question.split()
    triples = []
    
    for word in words:
        # 조사 및 특수문자 제거
        clean_word = re.sub(r'(은|는|이|가|을|를|에|으로|에서|부터|하고|요|다)$', '', word)
        clean_word = re.sub(r'[^\w\s]', '', clean_word)
        
        if len(clean_word) >= 2 and not re.match(r'^[0-9]+(세|주|번|월)', clean_word):
            # 중복 데이터 방지를 위해 set 등을 사용할 수 있으나 일단 리스트 유지
            rel = "has_symptom" if any(x in clean_word for x in ['진', '반', '통', '염', '증', '상', '질']) else "related_to"
            triples.append([head, rel, clean_word])
            
    return triples

# ==========================================
# 2. 메인 실행 로직
# ==========================================
all_triples = []

if not os.path.exists(folder_path):
    print(f"❌ 오류: '{folder_path}' 폴더를 찾을 수 없습니다.")
else:
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    print(f"📂 총 {len(file_list)}개의 파일을 찾았습니다. 분석 중...")

    for file_name in file_list:
        file_full_path = os.path.join(folder_path, file_name)
        try:
            # utf-8-sig는 BOM 제거를 위해 사용 (유지)
            with open(file_full_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                extracted = fast_triple_extractor(data)
                all_triples.extend(extracted)
        except Exception as e:
            print(f"⚠️ 파일 읽기 오류 ({file_name}): {e}")

    # 3. 결과 저장 (중복 생성 방지를 위해 'w' 모드로 덮어쓰기)
    if all_triples:
        try:
            # 중복 행 제거 (필요 시)
            unique_triples = list(set(tuple(x) for x in all_triples))
            
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(["Head", "Relation", "Tail"])
                writer.writerows(unique_triples)
            
            print(f"\n✅ 작업 완료! 저장 위치: {output_file}")
            print(f"📊 추출된 고유 트리플 개수: {len(unique_triples)}")
        except PermissionError:
            print(f"❌ 오류: '{output_file}'이 열려있습니다. 파일을 닫고 재실행하세요.")
    else:
        print("ℹ️ 추출된 데이터가 없습니다.")
