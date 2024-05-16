import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib


# Load the saved model
model = joblib.load('path_to_saved_model.pkl')

# Load the test data
test_data = pd.read_csv('path_to_test_data.csv')

# Preprocess the test data if needed

# Extract the features and target variables from the test data
X_test = test_data.drop('target_variable', axis=1)
y_test = test_data['target_variable']

# Make predictions using the loaded model
y_pred = model.predict(X_test)

# Calculate the RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"RMSE: {rmse}")