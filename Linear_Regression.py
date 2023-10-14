# Hypothesis
# We can predict how many medals a country will win at the Olympics by using historical data.


import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import numpy as np


teams = pd.read_csv("teams.csv")
teams = teams[["team", "country", "year", "athletes", "age", "prev_medals", "medals"]]
# teams.corr()["medals"] # we can see that the greatest correlation with medals is prev_medals column, so we are going to use prev_medals for our model


# sns.lmplot(x="age", y="medals", data=teams, fit_reg=True, ci=None) # We can see that there isn't a linear relationship between age and medals

teams = teams.dropna()  # get rid of 0 values to make our model accurate
train = teams[
    teams["year"] < 2012
].copy()  # Splitting our data up. We will only analyze the post 2012 Olympics data to make our data as accure as possible

test = teams[teams["year"] >= 2012].copy()

train.shape  # Display the number of values for our training set
test.shape  # Display the number of values for our testing set

reg = (
    LinearRegression()
)  # By importing sklearn module, we can initialize our linear regression
predictors = [
    "athletes",
    "prev_medals",
]  # We are going to use these columns for our prediction
target = "medals"  # We are going to predict this column using
reg.fit(
    train[predictors], train["medals"]
)  # Apply the Linear regression module to our values, by passing predictors and target columns
predictions = reg.predict(test[predictors])  # Predict our values using predictors
test["predictions"] = predictions  # Create new columns with these values
test.loc[
    test["predictions"] < 0, "predictions"
] = 0  # Initialize 0 to all values less than zero
test["predictions"] = test[
    "predictions"
].round()  # Round up all the prediction to the nearest whole number
error = mean_absolute_error(
    test["medals"], test["predictions"]
)  # Display how much on average we were within our actual values

teams.describe()[
    "medals"
]  # Make sure the error is smaller than our standart deviation which is the case for our data
test[
    test["team"] == "USA"
]  # Observe the USA case which shows that we are not absolutely correct, neither we are very far
errors = (test["medals"] - test["predictions"]).abs()  # Find the absolute error
error_by_team = errors.groupby(
    test["team"]
).mean()  # Group the mean of these values by countries
medals_by_team = test["medals"].groupby(test["team"]).mean()
error_ratio = (
    error_by_team / medals_by_team
)  # Find the reation between the error and the medals
error_ratio[~pd.isnull(error_ratio)]  # Elimanate zero values
error_ratio = error_ratio[np.isfinite(error_ratio)]  # Elimanate Infinite values
error_ratio.plot.hist()  # Present the information in a histgram
error_ratio.sort_values()  # See on what countries our value works the best


""" Conclusion: our model works teh best with the countires that have the most amount of medals """
