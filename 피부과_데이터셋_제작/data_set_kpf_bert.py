import json
import re
import os
import csv

base_path = os.getcwd() 
folder_path = os.path.join(base_path, "피부과_데이터셋_제작", "data")
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

    # 1. 정답(Head) 정제 로직 개선 (패턴 매칭 강화)
    head = ""
    # 앞의 "1) ", "2) " 등의 번호 포맷 제거
    clean_answer = re.sub(r'^[0-9]+\)\s*', '', answer).strip()

    # 패턴 A: "질병명(영어명)" 추출 시도
    match = re.search(r'([가-힣a-zA-Z0-9]+)\s*\([a-zA-Z\s\-]+\)', clean_answer)
    if match:
        head = match.group(1).strip()
    else:
        # 패턴 B: 괄호가 없는 경우 첫 단어 구역만 추출
        head = clean_answer.split(' (')[0].split('(')[0].split()[0].strip()
    
    # 2. 강력한 안전장치 (필터링)
    # 문장이 너무 길거나 노드명으로 부적합한 경우 제외
    if len(head) > 15 or "환자" in head or "증상" in head or head.endswith(('다.', '요.', '한다')):
        return []

    # 3. Tail 추출 로직 (단어 필터링 및 조사 제거 강화)
    words = question.split()
    triples = []

    for word in words:
        # 조사 및 특수문자 제거 (원본의 강화된 정규식 사용)
        clean_word = re.sub(r'(은|는|이|가|을|를|에|으로|에서|부터|하고|요|다|의|과|와)$', '', word)
        clean_word = re.sub(r'[^\w\s]', '', clean_word)
        
        # 2글자 이상이며, 숫자+단위가 아닌 단어만 추출
        if len(clean_word) >= 2 and not re.match(r'^[0-9]+(세|주|번|월|년|일|mm|cm|kg)', clean_word):
            # 관계 설정 (원본의 확장된 키워드 리스트 사용)
            rel = "has_symptom" if any(x in clean_word for x in ['진', '반', '통', '염', '증', '상', '질', '병', '암', '균']) else "related_to"
            triples.append([head, rel, clean_word])

    return triples

all_triples = []

if not os.path.exists(folder_path):
    print(f"❌ 오류: '{folder_path}' 폴더를 찾을 수 없습니다.")
else:
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    print(f"📂 총 {len(file_list)}개의 파일을 찾았습니다. 분석 중...")

    for file_name in file_list:
        file_full_path = os.path.join(folder_path, file_name)
        try:
            with open(file_full_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                extracted = fast_triple_extractor(data)
                all_triples.extend(extracted)
        except Exception as e:
            print(f"⚠️ 파일 읽기 오류 ({file_name}): {e}")

    # 3. 결과 저장
    if all_triples:
        try:
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