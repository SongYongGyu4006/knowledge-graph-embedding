import json
import re
import os
import csv

# ==========================================
folder_path = "./data"
output_file = "./result.csv"

def fast_triple_extractor(json_data):
    """JSON 데이터에서 Head, Relation, Tail을 추출하는 함수"""
    question = json_data.get("question", "")
    answer = json_data.get("answer", "")
    
    if not question or not answer:
        return []

    # 1. 정답(Head) 정제 로직 개선
    head = ""
    # 앞의 "1) ", "2) " 등의 번호 포맷 제거
    clean_answer = re.sub(r'^[0-9]+\)\s*', '', answer).strip()

    # 패턴 A: "질병명(영어명)" 또는 "질병명 (영어명)" 추출 (예: "건선(psoriasis)", "옴 (Scabies)")
    match = re.search(r'([가-힣a-zA-Z0-9]+)\s*\([a-zA-Z\s\-]+\)', clean_answer)
    if match:
        head = match.group(1).strip()
    else:
        # 패턴 B: 괄호가 없는 경우 기존처럼 첫 단어 구역만 추출 시도
        head = clean_answer.split(' (')[0].split('(')[0].split()[0].strip()
        # 2. 강력한 안전장치 (필터링)
        # 문장이 통째로 들어오거나, 노드명으로 부적합한 경우 해당 트리플은 과감히 버림(Drop)
    if len(head) > 15 or "환자" in head or "증상" in head or head.endswith(('다.', '요.', '한다')):
        return []

            # 3. Tail 추출 로직 (단어 필터링 강화)
    words = question.split()
    triples = []

    for word in words:
        # 조사 및 특수문자 제거
        clean_word = re.sub(r'(은|는|이|가|을|를|에|으로|에서|부터|하고|요|다|의|과|와)$', '', word)
        clean_word = re.sub(r'[^\w\s]', '', clean_word)

        # 2글자 이상이며, 숫자+단위(32세, 4주 등)가 아닌 단어만 추출
        if len(clean_word) >= 2 and not re.match(r'^[0-9]+(세|주|번|월|년|일|mm|cm|kg)$', clean_word):
            # 관계 설정
            rel = "has_symptom" if any(
                x in clean_word for x in ['진', '반', '통', '염', '증', '상', '질', '병', '암', '균']) else "related_to"
            triples.append([head, rel, clean_word])

    return triples

# ==========================================
# 2. 메인 실행 로직
# ==========================================
all_triples = []

# 경로 존재 여부 확인 전, 폴더가 없다면 메시지 출력
if not os.path.exists(folder_path):
    print(f"❌ 오류: '{folder_path}' 폴더를 찾을 수 없습니다. 저장소 내에 'skin_data' 폴더가 있는지 확인해주세요.")
else:
    # 폴더 내 모든 .json 파일 목록 가져오기
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    print(f"📂 총 {len(file_list)}개의 파일을 찾았습니다. 분석을 시작합니다...")

    for file_name in file_list:
        file_full_path = os.path.join(folder_path, file_name)
        with open(file_full_path, 'r', encoding='utf-8-sig') as f:
            try:
                data = json.load(f)
                extracted = fast_triple_extractor(data)
                all_triples.extend(extracted)
            except Exception as e:
                print(f"⚠️ 파일 읽기 오류 ({file_name}): {e}")

    # 3. 결과 저장 (CSV 파일 생성)
    if all_triples:
        try:
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(["Head", "Relation", "Tail"]) # 엑셀 헤더
                writer.writerows(all_triples)
            print(f"\n✅ 작업 완료! 결과가 저장되었습니다.")
            print(f"📍 저장 위치: {output_file}")
            print(f"📊 추출된 총 트리플 개수: {len(all_triples)}")
        except PermissionError:
            print(f"❌ 오류: '{output_file}'이(가) 이미 열려있습니다. 엑셀을 닫고 다시 실행해주세요.")
    else:
        print("ℹ️ 추출된 데이터가 없습니다. JSON 파일의 형식을 확인해주세요.")
