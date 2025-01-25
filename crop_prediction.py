# -*- coding: utf-8 -*-
"""Crop_prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_Lgo4gxxOokWxIAYngIXiyl75e3IAfiU
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense

# Load dataset (replace with your dataset file path)
data = pd.read_csv('/Users/prashantkumar/Drone_Ai/crop_prices2.csv')

# Display the first few rows of the dataset
print(data.head())

# Assuming the dataset has two columns: 'Date' and 'Price'
# Set the date as index (ensure the date column is in datetime format)
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Preprocessing: scaling the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data['Price'].values.reshape(-1, 1))

# Define sequence length (using past 60 days to predict the next)
sequence_length = 60

# Split data into training and testing sets (e.g., 80% train, 20% test)
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size - sequence_length:]  # To have overlap for sequence length

# Prepare training data
X_train = []
y_train = []
for i in range(sequence_length, len(train_data)):
    X_train.append(train_data[i-sequence_length:i, 0])
    y_train.append(train_data[i, 0])

X_train, y_train = np.array(X_train), np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Build the GRU model
model = Sequential()
model.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(GRU(units=50, return_sequences=False))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32)

# Prepare testing data
X_test = []
y_test = []
for i in range(sequence_length, len(test_data)):
    X_test.append(test_data[i-sequence_length:i, 0])
    y_test.append(test_data[i, 0])

X_test, y_test = np.array(X_test), np.array(y_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Make predictions on test data
predicted_prices = model.predict(X_test)
predicted_prices = scaler.inverse_transform(predicted_prices)  # Inverse scale to original prices
actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

# Visualization
plt.figure(figsize=(14, 5))
plt.plot(data.index[train_size:], actual_prices, color='blue', label='Actual Prices')
plt.plot(data.index[train_size:], predicted_prices, color='red', label='Predicted Prices')
plt.title('Grain/Crop Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

