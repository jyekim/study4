#43 카피함

import numpy as np 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM, GRU

#1. 데이터

dataset = np.array([1,2,3,4,5,6,7,8,9,10])   #데이터의 형태는 (10, )
#실질적으로 y는 없음
x = np.array ([[1,2,3], 
               [2,3,4], 
               [3,4,5], 
               [4,5,6],
               [5,6,7], 
               [6,7,8], 
               [7,8,9]])

y = np.array([4, 5, 6, 7, 8, 9, 10])

print(x.shape, y.shape)  #(7, 3) (7,)

x = x.reshape(7, 3, 1)
print(x.shape)           #(7, 3, 1)  ===> [[[1],[2],[3]], [2],[3],[4]],.....]

#2. 모델구성

model = Sequential()
# model.add(SimpleRNN(units=64, input_shape=(3, 1), activation='relu'))          #이부분이 rnn이 되는 것 
                                            #(N, 3, 1)--> ([batch, timesteps, feature])
# model.add(SimpleRNN(units=10, input_length=3, input_dim=1))  #timesteps를 input_lengh랑 같다는 것을 알 수 있다
# model.add(SimpleRNN(units= 64, input_dim=1, input_length=3))  #가독성이 떨어짐
# model.add(LSTM(units=64, input_length=3, input_dim=1))  
# model.add(LSTM(units=10, input_shape=(3,1)))  #timesteps를 input_lengh랑 같다는 것을 알 수 있다
model.add(GRU(units=10, input_shape=(3,1)))  #timesteps를 input_lengh랑 같다는 것을 알 수 있다
model.add(Dense(5, activation='relu'))
model.add(Dense(1))

    
model.summary()

#심플 120
#LSTM 480
#GRU 390


#64 * (64 + 1 + 1) =4224
#units * (feature + bias + units) = parameter 

