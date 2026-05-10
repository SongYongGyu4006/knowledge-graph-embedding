import json
import re
import os
import csv

# ==========================================
# 1. 경로 설정 (이 부분만 정확히 수정하세요)
# ==========================================
# JSON 파일들이 들어있는 폴더 경로
folder_path = r"C:\Users\MINJAE\Downloads\download\skin_data" 

# 결과가 저장될 파일 경로 (파일명 result.csv를 꼭 포함하세요)
output_file = r"C:\Users\MINJAE\Downloads\download\skin_data\result.csv" 

def fast_triple_extractor(json_data):
    """JSON 데이터에서 Head, Relation, Tail을 추출하는 함수"""
    question = json_data.get("question", "")
    answer = json_data.get("answer", "")
    
    if not question or not answer:
        return []

    # 정답(Head) 정제: "2) 피부묘기증 (dermographism)" -> "피부묘기증"
    head = re.sub(r'^[0-9]+\)\s*', '', answer).split(' (')[0].strip()
    
    # 단순 규칙 기반 엔티티 추출 (조사 및 특수문자 제거)
    words = question.split()
    triples = []
    
    for word in words:
        # 조사 제거 (한국어 특성 반영)
        clean_word = re.sub(r'(은|는|이|가|을|를|에|으로|에서|부터|하고|요|다)$', '', word)
        # 특수문자 제거
        clean_word = re.sub(r'[^\w\s]', '', clean_word)
        
        # 2글자 이상이며, 숫자+단위(32세, 4주 등)가 아닌 단어만 추출
        if len(clean_word) >= 2 and not re.match(r'^[0-9]+(세|주|번|월)', clean_word):
            # 관계 설정: 증상 관련 키워드가 포함되면 has_symptom으로 분류
            rel = "has_symptom" if any(x in clean_word for x in ['진', '반', '통', '염', '증', '상', '질']) else "related_to"
            triples.append([head, rel, clean_word])
            
    return triples

# ==========================================
# 2. 메인 실행 로직
# ==========================================
all_triples = []

if not os.path.exists(folder_path):
    print(f"❌ 오류: '{folder_path}' 경로를 찾을 수 없습니다. 폴더 경로를 다시 확인해주세요.")
else:
    # 폴더 내 모든 .json 파일 목록 가져오기
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    print(f"📂 총 {len(file_list)}개의 파일을 찾았습니다. 분석을 시작합니다...")

    for file_name in file_list:
        file_full_path = os.path.join(folder_path, file_name)
        # encoding='utf-8-sig'를 사용하여 BOM 오류를 원천 차단합니다.
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