# Github Copilot 
import pandas as pd
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import joblib

class TrainRF:
    def __init__(self, dataframe, target_column,param_grid=None, seed=12345, 
                        test_split=0.1, kfolds=5, error_metric='neg_root_mean_squared_log_error'):
        self.dataframe = dataframe
        self.target_column = target_column
        self.parameter_grid = param_grid
        self.seed = seed
        self.test_split = test_split
        self.kfolds = kfolds
        self.error_metric = error_metric
        self.best_model = None

    def train_model(self):
        # Split the dataframe into features and target
        X = self.dataframe.drop(columns=[self.target_column])
        y = self.dataframe[self.target_column]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_split, random_state=self.seed)

        # Initialize the model
        model = RandomForestRegressor(criterion="squared_error", random_state=self.seed)

        # Perform grid search
        grid_search = GridSearchCV(model, self.parameter_grid, cv=self.kfolds, 
                                    scoring = self.error_metric, n_jobs=-1, verbose=2, return_train_score=True)
        grid_search.fit(X_train, y_train)

        # Get all cross validation results
        cv_results = pd.DataFrame(grid_search.cv_results_)

        # Get the best parameters and best score
        best_params = grid_search.best_params_
        best_score = grid_search.best_score_

        # Initialize the model with the best parameters
        best_model = RandomForestRegressor(**best_params)

        # Train the model
        best_model.fit(X_train, y_train)

        # Evaluate the model on the train set
        train_pred = best_model.predict(X_train)
        train_score = root_mean_squared_error(y_train, train_pred)

        # Evaluate the model on the test set
        test_pred = best_model.predict(X_test)
        test_score = root_mean_squared_error(y_test, test_pred)

        # Set best model as attribute
        self.best_model = best_model

        return best_model, train_score, test_score, cv_results

    def save_best_model(self, file_path):
        # Save the model to the given file path
        joblib.dump(self.best_model, file_path, compress=1)