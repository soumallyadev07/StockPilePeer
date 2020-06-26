from flask import Flask,render_template,request
#Libraries
import math
from datetime import date
import datetime
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import re
plt.style.use('fivethirtyeight') 

app = Flask(__name__)
today = date.today()
tomorrow = today + datetime.timedelta(days = 1)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/predict', methods=['POST',  'GET'])
def predict():
	comname = request.form['companyname']
	companyname = str(comname)
	df = web.DataReader(companyname, data_source='yahoo', start='2012-01-01', end=str(today))
	#Visualizing the data(Close Price)
	# plt.figure(figsize=(16,8))
	# plt.title('Close Price History')
	# plt.plot(df['Close'])
	# plt.xlabel('Data', fontsize=18)
	# plt.ylabel('Close Price', fontsize=18)
	# fig1 = plt.gcf()
	# plt.show()
	# fig1.savefig('graph.png')
	data = df.filter(['Close'])
	dataset = data.values
	training_data_len = math.ceil(len(dataset)*0.8)
	scaler = MinMaxScaler(feature_range=(0,1))
	scaled_data = scaler.fit_transform(dataset)
	train_data = scaled_data[0:training_data_len, :]
	x_train = []
	y_train = []
	for i in range(60, len(train_data)):
		x_train.append(train_data[i-60:i, 0])
		y_train.append(train_data[i,0])

	
	x_train, y_train = np.array(x_train), np.array(y_train)
	x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

	
	model = Sequential()
	model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1],1)))
	model.add(LSTM(50, return_sequences=False))
	model.add(Dense(25))
	model.add(Dense(1))

	
	model.compile(optimizer='adam', loss='mean_squared_error')

	
	model.fit(x_train, y_train, batch_size=1, epochs=1)
	
	
	test_data = scaled_data[training_data_len - 60: , :]
	
	x_test = []
	y_test = dataset[training_data_len:, :]
	for i in range(60, len(test_data)):
		x_test.append(test_data[i-60:i, 0])
	
	x_test = np.array(x_test)
	x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
	
	#Get Model's predicted Values
	predictions = model.predict(x_test)
	predictions = scaler.inverse_transform(predictions)
	
	#Get the quote
	company_quote = web.DataReader(companyname, data_source='yahoo', start='2012-01-01', end=str(today))
	#Create a new Dataframe
	new_df = company_quote.filter(['Close'])
	#Get the Last 60 days Closing Prices and convert the dataframe into an array
	last_60_days = new_df[-60:].values
	#Scale the data
	last_60_days_scaled = scaler.transform(last_60_days)
	#Create an empty list
	X_test = []
	#Append the past 60 days
	X_test.append(last_60_days_scaled)
	#convert the X_test data set to a numpy array
	X_test = np.array(X_test)
	#Reshape the data
	X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
	#Get the predicted Scaled Price
	pred_price = model.predict(X_test)
	#undo the scaling
	pred_price = scaler.inverse_transform(pred_price)
	predictionprice = str(pred_price)
	predictionpricestr = re.sub(r" ?\([^)]+\)", "", predictionprice)
	return render_template('index.html', pred='Our prediction for {} on {} is {}'.format(companyname, tomorrow, predictionpricestr))

if __name__ == '__main__':
	app.run()
