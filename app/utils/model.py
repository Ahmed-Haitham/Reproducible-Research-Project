# Github Copilot was used to comment the code
import pickle
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error

class Model:
    def __init__(self, model_file, data, target_column, seed=12345, test_split=0.1):
        self.model_file = model_file
        self.data = data
        self.target_column = target_column
        self.seed = seed
        self.test_split = test_split
        self.model = None
        self.model_fit = None
        self.model_predict = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def load_model(self):
        # Load the trained model from the model file
        self.model = joblib.load(self.model_file)

    def prepare_data(self):
        # Prepare the data for training and testing

        # Drop the target column and its corresponding log-transformed column from the data
        if self.target_column == 'fare_amount':
            X = self.data.drop(columns=[self.target_column,'fare_amount_log'])
        elif self.target_column =='fare_amount_log':
            X = self.data.drop(columns=[self.target_column,'fare_amount'])
        
        y = self.data[self.target_column]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_split, random_state=self.seed)

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def fit_model(self):
        # Fit the model to the training data
        self.model_fit = self.model.fit(self.X_train, self.y_train)
        return self.model_fit

    def predict(self, X_test):
        # Make predictions on the test data
        self.model_predict = self.model.predict(X_test)
        return self.model_predict

    def train_score(self):
        # Calculate the root mean squared error on the training data
        train_pred = self.model.predict(self.X_train)
        train_score = root_mean_squared_error(self.y_train, train_pred)
        return train_score
    
    def test_score(self):
        # Calculate the root mean squared error on the test data
        test_pred = self.model.predict(self.X_test)
        test_score = root_mean_squared_error(self.y_test, test_pred)
        return test_score
