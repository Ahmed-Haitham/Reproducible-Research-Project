from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

# Load your data
data = datasets.load_boston()
X = data.data
y = data.target

# Define your model specification
model = xgb.XGBRegressor()

# Define the pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),  # Optional: Apply feature scaling
    ('model', model)
])

# Perform cross-validation
cv_results = cross_val_score(pipeline, X, y, cv=cv_folds, scoring=make_scorer(mean_squared_error))

# Fit the pipeline to the data
pipeline.fit(X, y)

# Get the trained model
trained_model = pipeline.named_steps['model']

# Return the cross-validation results and trained model
cv_results, trained_model
