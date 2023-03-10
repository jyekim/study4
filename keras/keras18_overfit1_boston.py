from sklearn.datasets import load_boston
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

#1.  데이터
datasets = load_boston()
x = datasets.data
y = datasets.target

print(x.shape, y.shape)   #. (506, 13) (506,)

x_train , x_test, y_train , y_test = train_test_split(
    x, y, shuffle=True, random_state=333, test_size=0.2) #. 506 *0.8 


#2. 모델구성 
model = Sequential()
#model.add(Dense(5, input_dim=13))    #.  input_dim  은 행과열로 있을때만 가능
model.add(Dense(5, input_shape=(13,)))    #.   4차원 같은 경우에는 input_shape로 써야함    위에 주석과 동일함
model.add(Dense(4))   
model.add(Dense(3))    
model.add(Dense(2))    
model.add(Dense(1))  


#.컴파일 ,훈련 

model.compile(loss='mse', optimizer='adam')

hist = model.fit(x_train, y_train, epochs=200, batch_size=1, 
          validation_split=0.2, verbose=1)   #. verbose는 함수 수행시 발생하는 상세한 정보들을 표준 출력으로 자세히 내보낼것인가 나타냄, 
                                            #. 0은 출력하지 않고, 1은 자세히, 2는 함축적인 정보만 출력하는 형태 3은 에포만 나옴
                                                                               
#4. 평가 예측
loss = model.evaluate(x_test, y_test)
print('loss : ', loss)
#verbose 1  걸린시간
print( "=================================")
print(hist)  #<keras.callbacks.History object at 0x000001762F26B5B0>\
print("==================================")
print(hist.history)      # dictionary 키 value 형태로 되어 있다. list형태 2개이상 /반환값 안에는  loss와 valloss의 dictionary히스토리에 제공된 변수가 있다는 뜻 
print("==================================")
print(hist.history['loss'])      
print("==================================")
print(hist.history['val_loss'])     


# 한글 폰트 넣기 
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.family'] ='Malgun Gothic'

mpl.rcParams['axes.unicode_minus'] =False





plt.figure(figsize=(9,6))     #.리스트 형태로 순서대로 되어 있는 것은  x를 명시 안해도 상관없다. 즉, y 만 넣어주면 됨
plt.plot(hist.history['loss'], c= 'red', marker='.', label='loss')
plt.plot(hist.history['val_loss'], c= 'blue', marker='.', label='val_loss')
plt.grid() #격자
plt.xlabel('epochs')
plt.ylabel('loss')
plt.title('보스톤 손실함수')               # matplotlib  그림에서 한글 깨짐 수정하기 
plt.legend()   # 라벨값이 명시됨
#plt.legend(loc='upper left')   
plt.show()


