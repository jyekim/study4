import numpy as np                     
from sklearn.datasets import fetch_covtype
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


#1.  데이터
datasets = fetch_covtype()
x = datasets.data
y = datasets['target']
print(x.shape, y.shape)   #(581012, 54) (581012,)
print(np.unique(y, return_counts=True))      #(array([1, 2, 3, 4, 5, 6, 7]), array([211840, 283301,  35754,   2747,   9493,  17367,  20510], dtype=int64)


import pandas as pd
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder()
#쉐이프를 맞추는 작업 
ohe.fit_transform(df.degree.values.reshape(-1,1)).toarray()
ohe = OneHotEncoder(drop='first')
ohe.fit_transform(df.degree.values.reshape(-1,1)).toarray()                     
y= ohe.fit_transform(y)
# from tensorflow.keras.utils import to_categorical 
# y = to_categorical(y) #원핫인코딩
print(y)
print(y.shape)  #(581012, 8)


x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                    shuffle=True, random_state=222, test_size=0.2, stratify=y)

#2. 모델구성 
model = Sequential()
model.add(Dense(5, activation= 'relu', input_shape=(54, )))
model.add(Dense(20, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(7, activation= 'softmax'))

#3.컴파일, 훈련 
from tensorflow.keras.callbacks import EarlyStopping

model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics=['accuracy'])          
earlystopping = EarlyStopping(monitor='val_loss', mode='min', patience=10, restore_best_weights=True, verbose=1)
import time
start = time.time()
model.fit(x_train, y_train, epochs=100, batch_size=128, 
          validation_split=0.2, callbacks=[earlystopping], verbose=1)
end = time.time()
print('걸린시간 : ', end- start)

#4. 평가 예측 
loss, accuracy = model.evaluate(x_test, y_test)
print('loss : , loss')  
print('accuracy : ', accuracy)                              

# print(y_test[:5])                                                       
# y_predict = model.predict(x_test[:5]) 
# print(y_predict)                                          


from sklearn.metrics import accuracy_score
import numpy as np                                                            

y_predict = model.predict(x_test)     
y_predict =np.argmax(y_predict, axis=1)   
print('y_pred(예측값) :', y_predict)
y_test =np.argmax(y_test, axis=1)     # 가장 큰 값을 찾아내는 것 
print('y_test(원래값) : ', y_test)  
print(y_predict)


acc = accuracy_score(y_test, y_predict)
print(acc)
