import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.model_selection import StratifiedShuffleSplit

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer

housing = pd.read_csv("data.csv")
train_set, test_set  = train_test_split(housing, test_size=0.2, random_state=42)

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)


for train_index, test_index in split.split(housing, housing['CHAS']):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

housing = strat_train_set.copy()
housing_test = strat_test_set.copy()

# housing = strat_train_set.drop("MEDV", axis=1)
housing_labels = strat_train_set["MEDV"].copy()

imputer = SimpleImputer(strategy="median") #In case of missing values(Can check by randomly removing comments)
imputer.fit(housing)

X = imputer.transform(housing)

housing_tr = pd.DataFrame(X, columns=housing.columns)

my_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="median")),
    #     ..... add as many as you want in your pipeline
    ('std_scaler', StandardScaler()),
])

housing_num_tr = my_pipeline.fit_transform(housing)
model = LinearRegression()
model2 = RandomForestRegressor()
model.fit(housing_num_tr, housing_labels)
model2.fit(housing_num_tr, housing_labels)

housing_predictions = model.predict(housing_num_tr)
housing_predictions2 = model2.predict(housing_num_tr)
mse = mean_squared_error(housing_labels, housing_predictions)
mse2 = mean_squared_error(housing_labels,housing_predictions2)
rmse = np.sqrt(mse)
rmse2 = np.sqrt(mse2)
# print(housing_predictions)
# print(housing_predictions2)
# print(housing_labels)

housing_predictions.reshape(1,404)
housing['predicted1'] = housing_predictions
housing['predicted2'] = housing_predictions2
# print(housing_predictions.shape)
# print(housing_predictions)
np.savetxt('data.csv', housing_predictions, delimiter=',', fmt='%d')
print(f"{housing}")
# print(rmse) # Linear Regression model
# print(rmse2) # Random Forest Model