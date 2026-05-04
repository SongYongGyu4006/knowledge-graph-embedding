# knowledge-graph-embedding
지식그래프 임베딩 해보기

# 참고!!
작업을 하면서 새로운 라이브러리 설치가 필요하기 때문에.. 실행이 안된다면 콘다 환경 생성을 다시 해주세요. 제가 버전 올릴 때마다 환경 업데이트 해두겠습니다.
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

# TransE1.0.0!!
아기다리 고기다리 TransE1.0.0을 샘플데이터에 학습 시키고 지식 그래프를 차원 축소하여 시각화까지 마쳤습니다.
### 모델정의
pykeen에서 제공하는 pipeline 함수는 자동으로 파라미터값을 맞춰주기 때문에, 간단하게 모델을 정의할 수 있었습니다.
```
result = pipeline(
    dataset='nations',
    model='TransE',
    # 모델 설정
    model_kwargs=dict(
        embedding_dim=50, # 임베딩 차원
        scoring_fct_norm=1, # L1 거리 공식 사용
    ),
    device=device,
    # 학습 설정
    training_kwargs=dict(
        num_epochs=100, # 에폭 수
        batch_size=64, # 배치 크기
        use_tqdm=True,
    ),
    # 정규화 설정
    optimizer_kwargs=dict(lr=1e-2),
)
```
애를 먹었던건 성능 평가였는데, MRR과 Hits@10을 측정할 때, result에서 나오는 키값이 pykeen의 버전에 따라 계속 바뀌어서.. 한참을 찾았습니다.

또한, 현재는 시각화를 matplotlib와 seaborn을 사용했는데, 2차원 산점도론 확 와닿지 않는 결과인것 같습니다.

### 객체 임베딩 시각화
<img width="1312" height="1176" alt="image" src="https://github.com/user-attachments/assets/c084963b-feec-4b28-bfa8-d9937d44fa35" />

### 관계 임베딩 시각화
<img width="1112" height="976" alt="image" src="https://github.com/user-attachments/assets/ce29ba21-5d68-41bc-ab66-cf92c9ba2d47" />




