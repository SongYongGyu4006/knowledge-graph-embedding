# knowledge-graph-embedding
지식그래프 임베딩 해보기

## 환경 설치법
모두 conda는 사용해보셨을거에요! 딥러닝이나 데이터 분석같은 경우 venv를 사용하는 것보단 conda를 사용하는게 더 안정적이에요.

아시다시피 pykeen 라이브러리 설치를 해야하는데, pykeen도 일종의 딥러닝이여서 sklearn도 설치를 했습니다.(파이썬 3.12.x, numpy 2.0이하 필수)

근데, 어차피 제가 환경을 추출해뒀으니 여러분은 아래 프로젝트 파일에서 명령어만 실행시키면 될거에요. (conda는 미리 설치해주세요)
```
#콘다 환경 생성. KGE는 KnowledgeGraphEmbeddig 약자입니다.
conda KGE create -f environment.yml
#콘다 환경 실행
conda activate KGE
```
실행은.. 간단하게
```
python main.py
```

