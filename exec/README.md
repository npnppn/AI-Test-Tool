
# README

제품불량 검사시 자동 Segmentation을 위한 Deep learning Tool  

*Dataset관련해서는 깃랩 용량부족으로 올릴 수가 없습니다.  

### 주요기능 
- 학습시 준비한 이미지의 크기 및 색상 등의 통일이 없어도 학습을 가능하게 해주는 이미지전처리 기능
- IOU 및 loss 수치 도출 
- 학습한 모델 사용하여 출력된 사진 및 test시 사용한 이미지/라벨 비교하기 편한 UI/UX  
- 서로 다른 학습 모델 비교 기능


### 환경설정
```
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
```


### 사용설명서
##### 라이브러리 설치
``` 
anaconda prompt 기준
conda create -n AI_sem python==3.8
conda install tensorboard 
conda install matplotlib
conda install Pillow
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```

##### 이미지 저장 경로 
``` 
### 이미지 파일과 라벨 파일의 수와 이름이 순서대로 매칭되어야 함 ###
./datasets/Imgs/ => 경로에 이미지 파일 저장
./datasets/labels/ => 경로에 라벨 파일 저장
```

##### 실행방법 
1. conda activate AI_sem
2. python main.py => main.py를 실행시켜 준다 

## 메인화면
![image](/uploads/d7f4d2c1803392297ddc8b594ef67fb1/image.png)  


## 전처리 
![image](/uploads/5f8d676cb7d0fa6da5994a979a562287/image.png)
- 이미지 저장 경로에 학습을 원하는 이미지와 라벨을 넣어주고 전처리 버튼을 클릭
- test/train/label 폴더가 생성되고 각각의 폴더 안에 .npy 파일 생성
- 학습하기로 이동



## 학습하기  
![image](/uploads/bd32c9c31aa426e2e71ccbf2a7932138/image.png)
- 전처리 후 학습모델에 이름 기재
- Hyperparameter(learningrate/epoch/batchsize) 적절하게 설정
- 학습시작 
- 학습 완료 후 Test하기로 이동 


## Test
![image](/uploads/e9f3678dd2514bc0cb6fb8dc1fb19024/image.png)
- 원하는 학습 모델을 선택한 뒤 Test 버튼 클릭
- 해당 모델의 테스트 데이터셋 결과 확인
- 원하는 학습 모델을 선택한 뒤 log 버튼 클릭하여 해당 모델의 tensorboard 확인



## Test비교하기
![image](/uploads/05a9d216ecf6c00e1078660249b18e00/image.png)
- 2개의 모델을 선택한 뒤 compare 버튼 클릭
- 2개의 모델의 테스트 데이터셋 결과 확인


## TensorBoard를 통해 학습&테스트 진행내용 확인  
![image](/uploads/0c7945353cdc7a62ad762ca4d6256fb3/image.png)  
![image](/uploads/1dd7c6d86720697698e41ef75fd87e66/image.png)
