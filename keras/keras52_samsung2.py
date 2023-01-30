#LSTM구성하기
import numpy as np                      
import pandas as pd              
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
# #numpy 데이터 불러오기 
# samsung = np.load('./_data/samsung.npy')
# amore = np.load('./_data/amore.npy')

# print(samsung)
# print(amore)
# print(samsung.shape)
# print(amore.shape)


#1. 데이터 
path = './_data/samsung/'
df1 = pd.read_csv(path + 'amore.csv', index_col=0,
                  header=0, encoding='cp949', sep=',',thousands=',')
print(df1)
print(df1.shape)    #(1980, 16)

df2 = pd.read_csv(path + 'samsung.csv', index_col=0,
                  header=0, encoding='cp949', sep=',', thousands=',')
print(df2)
print(df2.shape)   #(2221, 16)
print(df1.dtypes)

df1 = df1[['시가','종가','저가','고가','거래량']]
df2 = df2[['시가','종가','저가','고가','거래량']]

df1.isnull().any()    #null값이 어느 열에 있는지

df1 = df1[df1['시가'] < 1000000] #시가 백만원 이하가 있는거만 남기는것 

# # 삼성전자의 모든 데이터
# for i in range(len(df1.index)):       # 거래량 str 을 int 변경
#          for j in range(len(df1.iloc[i])):
#                 df1.iloc[i,j] = int(df1.iloc[i,j].replace(',', ''))
# # 아모레의 모든 데이터
# for i in range(len(df2.index)):
#          for j in range(len(df2.iloc[i])):
#                 df2.ilocp[i,j] = int(df2.iloc[i,j].replace(',', ''))          


#일자 오름차순(최근날짜를 가장 아래로)
df1 = df1.sort_values(['일자'], ascending=[True])
df2 = df2.sort_values(['일자'], ascending=[True]) 
print(df1)
print(df2)
  
  
#pandas를 numpy로 변경 후 저장
df1 = df1.values
df2 = df2.values
print(type(df1), type(df2))
print(df1.shape, df2.shape)    #(2220, 16) (1980, 16)

np.save('./_data/samsung.npy', arr=df1)
np.save('./_data/amore.npy', arr=df2)


#numpy 데이터 불러오기 
samsung = np.load('./_data/samsung.npy',allow_pickle=True)
amore = np.load('./_data/amore.npy', allow_pickle=True)

print(samsung)
print(amore)
print(samsung.shape)
print(amore.shape)


# dnn 구성하기 
def split_xy5(dataset, time_steps, y_column):
    x, y = list(), list()
    for i in range(len(dataset)):
        x_end_number = i + time_steps
        y_end_number = x_end_number + y_column 

        if y_end_number > len(dataset):  
            break
        tmp_x = dataset[i:x_end_number, :]  
        tmp_y = dataset[x_end_number:y_end_number, 0]  
        x.append(tmp_x)
        y.append(tmp_y)
    return np.array(x), np.array(y)
x1, y1 = split_xy5(samsung, 5, 1) 
x2, y2 = split_xy5(amore, 5, 1) 
print(x2[0,:], "\n", y2[0])
print(x2.shape)
print(y2.shape)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    x1, y1, random_state=1, test_size= 0.3)
print(x_train.shape)  #(1550, 5, 5)
print(x_test.shape)    #(665, 5, 5)
print(y_train.shape)    #(1550, 1)
print(y_test.shape)     #(665, 1)

# #####데이터 전처리####
# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# scaler.fit(x_train)
# x_train_scaled = scaler.transform(x_train)
# x_test_scaled = scaler.transform(x_test)
# print(x_train_scaled[0, :])

#2 모델구성 
model = Sequential()
model.add(LSTM(64, input_shape=(5, 5), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(1))
model.summary()  


#3.컴파일 ,훈련

model.compile(loss='mse', optimizer='adam', metrics=['mse'])

from tensorflow.keras.callbacks import EarlyStopping    
earlystopping = EarlyStopping(monitor='val_loss', mode='min', 
                              patience=10, restore_best_weights=True, verbose=1)    #loss 를 할지 val_loss로 할지 선택 가능 loss는 무조건 min accuracy는 max로 하면됨
                                            #멈추기 시작한 자리; 브레이크 한 시점의 웨이트가 저장된다.  patience 너무 크게 잡으면 빨리 끝나버림 

model.fit(x_train, y_train, epochs=200, 
          validation_split=0.2, callbacks=[earlystopping], verbose=1)

loss, mse = model.evaluate(x_test, y_test, batch_size=1)
print('loss :', loss)
print('mse :', mse)

y_pred = model.predict(x_test)
for i in range(5):
        print('시가 : ', y_test[i], '/ 예측가 : ', y_pred[i])


"""

시가 :  [299000.] / 예측가 :  [300699.7]
시가 :  [323500.] / 예측가 :  [325580.62]
시가 :  [234500.] / 예측가 :  [238669.73]
시가 :  [163500.] / 예측가 :  [164235.44]
시가 :  [126500.] / 예측가 :  [128229.53]
"""

"""
#2. 모델구성
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
#2-1 모델 
input1 = Input(shape=(2,))
dense1 = Dense(11, activation='relu', name='ds11')(input1)
dense2 = Dense(12, activation='relu', name='ds12')(dense1)
dense3 = Dense(13, activation='relu', name='ds13')(dense2)
output1 = Dense(14, activation='relu', name='ds14')(dense3)
#2-2 모델 2
input2 = Input(shape=(3,))
dense21 = Dense(21, activation='linear', name='ds21')(input2)
dense22 = Dense(22, activation='linear', name='ds22')(dense21)
output2 = Dense(23, activation='linear', name='ds23')(dense22)
#2-3 모델병합
from tensorflow.keras.layers import concatenate
merge1 = concatenate([output1, output2], name ='mg1')
merge2 = Dense(12, activation= 'relu', name ='mg2')(merge1)
merge3 = Dense(13, name ='mg3')(merge2)
last_output = Dense(1, name='last')(merge3)#여기서 1은 y를 뜻함 그래서 1개임
model = Model(inputs=[input1, input2], outputs=last_output)
model.summary()
#3. 컴파일 훈련 
model.compile(loss ='mse', optimizer='adam')
model.fit([x1_train, x2_train], y_train, epochs=10, batch_size=8)
#4. 평가 예측
loss = model.evaluate([x1_test, x2_test], y_test)
print('loss : ', loss)                              """      