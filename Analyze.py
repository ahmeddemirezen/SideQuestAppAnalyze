from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd

def StringToFloat(string):
    if(string.find('k') != -1):
        return float(string.replace('k', '')) * 1000
    elif(string.find('M') != -1):
        return float(string.replace('M', '')) * 1000000
    else:
        return float(string)

'''
    demo 0
    free 1
    opensource 2
    paid 3
    paidprerelease 4
    prerelease 5
'''
def get_type(string):
    if(string.find('demo') != -1):
        return 0
    elif(string.find('free') != -1):
        return 1
    elif(string.find('opensource') != -1):
        return 2
    elif(string.find('paid') != -1):
        return 3
    elif(string.find('paidprerelease') != -1):
        return 4
    elif(string.find('prerelease') != -1):
        return 5
    else:
        return -1

df = pd.read_csv('sidequest.csv')


df = df.dropna()





# clear data

df['click'] = df['click'].apply(lambda x: StringToFloat(x))
df['view'] = df['view'].apply(lambda x: StringToFloat(x))
df['price_type'] = df['price_type'].apply(lambda x: get_type(x))

y = df.click
features = ['view', 'rating', 'rating_count', 'price_type']
myTestInputs = pd.DataFrame(columns=features)
myTestInputs['view'] = [10000]
myTestInputs['rating'] = [4]
myTestInputs['rating_count'] = [110]
myTestInputs['price_type'] = [3]
X = df[features]

## Train Model
x_train, x_test, y_train, y_test = train_test_split(X,y,random_state=1)

model = DecisionTreeRegressor(random_state=1)
model.fit(x_train, y_train)

predictions = model.predict(x_test)
mean_absolute_error(y_test, predictions)

results = pd.DataFrame()

results["True"] = y_test
results["Pred"] = predictions
results["Diff"] = results.apply(lambda x: x["True"] - x["Pred"],axis=1)

print(results.describe())
print(model.score(x_test, y_test))

results.to_csv('results.csv')

## Full Model

fullModel = DecisionTreeRegressor(random_state=1)
fullModel.fit(X, y)
print(fullModel.predict(myTestInputs))



