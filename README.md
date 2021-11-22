
# 🌎 PAI (Personal AI)


>   AI를 몰라도 누구나 쉽게 AI 모델 학습 및 테스트가 가능한 Tool 개발


## 👨‍👩‍👧‍👦 팀원
 🧡 **김다윗**  
 💛 **권도엽**  
 💚 **박형민**  

## 🎥 프로젝트 개요
### 진행 기간
- 2021.10.11 ~ 2021.11.19 (6주)

### 주제
- 제품불량 검사시 자동 Segmentation을 위한 Deep learning Tool 개발

### 목표
입력 영상에 대해 자동으로 학습 데이터 (불량 Mask)를 생성할 수 있는 Segmentation 기반 Tool을 개발함으로써 데이터의 정확성을 향상시키고 학습 데이터 생성 시간을 단축


### 프로젝트 RULE
1. Jira를 사용하여 1주일 단위의 스프린트를 진행하고 프로젝트를 관리한다.
2. 매일 오전과 오후에 스크럼 미팅, wrap up을 실시하고 기록한다.
3. 리뷰는 가감없이 하되, 항상 배려와 존중의 태도로 임한다.
4. 정한 git commit 규칙을 준수하여 프로젝트 형상 관리를 한다.
5. Git Convention, Jira Convention, Code Convention 을 준수하여 개발을 진행한다.


### 와이어프레임
![](https://i.imgur.com/vmDp1b0.png)

![](https://i.imgur.com/zJcIK7E.png)




<br>

## 🍀 핵심기능
 1) 학습시 준비한 이미지의 크기 및 색상 등의 통일이 없어도 학습을 가능하게 해주는 이미지전처리 기능
 2) IOU 및 loss 수치 도출 
 3) 학습한 모델 사용하여 출력된 사진 및 test시 사용한 이미지/라벨 비교하기 편한 UI/UX  
 4) 서로 다른 학습 모델 비교 기능

<br>

## 📚 Tech Stack
Python  
AI


## 📊 서비스 구조도
![](https://i.imgur.com/4bQimqm.png)




## 💻 개발환경
conda 4.10.3  
python = 3.8.0  
pytorch = 1.7.0  
cudatoolkit = 11.3.1  
numpy = 1.21.2   
tensorboard = 2.7.0  
matplotlib = 3.1.1  
Pillow = 8.4.0  
PyQt5 = 5.15.6  
opencv-python = 4.5.4.58  
pip = 21.3.1  
pyinstaller = 4.7  


## 💻 사용설명서
### 라이브러리 설치
``` 
anaconda prompt 기준
conda create -n AI_sem python==3.8
conda install tensorboard 
conda install matplotlib
conda install Pillow
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```

### 이미지 저장 경로 
``` 
### 이미지 파일과 라벨 파일의 수와 이름이 순서대로 매칭되어야 함 ###
./datasets/Imgs/ => 경로에 이미지 파일 저장
./datasets/labels/ => 경로에 라벨 파일 저장
```

### 실행방법 
1. conda activate AI_sem
2. python main.py => main.py를 실행시켜 준다 

### 메인화면
![](https://i.imgur.com/MYaWISC.png)



## 전처리 
![](https://i.imgur.com/5aOaljw.png)

- 이미지 저장 경로에 학습을 원하는 이미지와 라벨을 넣어주고 전처리 버튼을 클릭
- test/train/label 폴더가 생성되고 각각의 폴더 안에 .npy 파일 생성
- 학습하기로 이동




## 학습하기  
![](https://i.imgur.com/KbaB1on.png)

- 전처리 후 학습모델에 이름 기재
- Hyperparameter(learningrate/epoch/batchsize) 적절하게 설정
- 학습시작 
- 학습 완료 후 Test하기로 이동 




## Test
![](https://i.imgur.com/rbtVarZ.png)

- 원하는 학습 모델을 선택한 뒤 Test 버튼 클릭
- 해당 모델의 테스트 데이터셋 결과 확인
- 원하는 학습 모델을 선택한 뒤 log 버튼 클릭하여 해당 모델의 tensorboard 확인




## Test비교하기
![](https://i.imgur.com/PTe9P19.png)

- 2개의 모델을 선택한 뒤 compare 버튼 클릭
- 2개의 모델의 테스트 데이터셋 결과 확인




## TensorBoard를 통해 학습&테스트 진행내용 확인  
![](https://i.imgur.com/8JSYtMt.png)

![](https://i.imgur.com/OuonPwV.png)


