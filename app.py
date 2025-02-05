import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
import yfinance as yf             
from keras.models import load_model
import streamlit as st         

start = '2010-01-01'
end = '2023-12-31'


st.title("Stock Trend Predictions (Closing Price)")


stock_input = st.text_input('Enter Stock','AAPL')

df = yf.download(stock_input, start, end)

#describing the data to user

st.subheader('Data from 2010 - 2023')

st.write(df.describe())


#visualizing the data

st.subheader('Closing Price vs Time')
fig = plt.figure(figsize=(12,6))
plt.plot(df.Close)
st.pyplot(fig)


st.subheader('Closing Price vs Time with 100 Moving Average')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)


st.subheader('Closing Price vs Time with 100 Moving Average and 200 Moving Average')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12,6))
plt.plot(ma100,'r')
plt.plot(ma200,'b')
plt.plot(df.Close,'g')
st.pyplot(fig)



#splitting data into training and testing

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0,1))

data_training_array = scaler.fit_transform(data_training)


#loading the keras model

model = load_model('stock_model.h5')



#Testing the Model
past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])

x_test = np.array(x_test)
y_test = np.array(y_test)

y_predicted = model.predict(x_test)

scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor


#final visualization
st.subheader('Predicted vs Real Prices')
fig2 = plt.figure(figsize = (12,6))
plt.plot(y_test,'b', label = 'Original Price')
plt.plot(y_predicted,'r',label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)


# Analysis logic: if 100 days MA crosses above 200 days MA then there is an uptrend



#streamlit run app.py to start