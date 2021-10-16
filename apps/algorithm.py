import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split
from sklearn.preprocessing import OrdinalEncoder,  MinMaxScaler, StandardScaler

df.drop_duplicates(keep='first', inplace=True)
df_cats = df.select_dtypes(include=['object']).copy()
for i in df_cats.columns:
    mode = df_cats[i].mode()[0]
    df[i].replace('unknown',mode, inplace=True)
df['y'].replace(['no', 'yes'],[0,1], inplace=True)
df.rename(columns={"y":"subscribe"}, inplace=True)
np.random.seed(42)
#Modeling
enc = OrdinalEncoder()
df_cat = df.select_dtypes(include='object')
df_cats = df_cat.columns.tolist()
enc.fit(df[df_cats])
df[df_cats] = enc.transform(df[df_cats])
df_model = df[["subscribe", "contact", "duration","pdays","previous", "poutcome","emp.var.rate", "cons.price.idx","euribor3m", "nr.employed"]]
X =  df_model.drop(['subscribe'],axis=1)
y = df_model['subscribe']

#split data to train ,test and sample
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42, stratify = y)

scaler = StandardScaler()
X_train_trf = scaler.fit_transform(X_train)
X_test_trf = scaler.transform(X_test)

#Define Model
try:
    import xgboost as xgb
except ImportError as ex:
    print("Error: the xgboost library is not installed.")
    xgboost = None

if xgb is not None: 
    xgb_model = xgb.XGBClassifier(verbosity = 0)

warnings.simplefilter(action='ignore', category=UserWarning)
#train the model with our data train
xgb_model.fit(X_train_trf, y_train)
predictions_XGB = xgb_model.predict(X_test_trf)

#Tuning
warnings.simplefilter(action='ignore', category=UserWarning)
C = [0.1, 0.5, 1]
solver = ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']
verbose = [1, 2, 3]
params_grid = {'C': C,
               'solver': solver,
               'verbose': verbose}

model_log = xgb.XGBClassifier(verbosity = 0)
model_log_gridCV = GridSearchCV(model_log, params_grid, scoring="f1", cv=3, verbose=2, n_jobs=-1)

model_log_gridCV.fit(X_train_trf, y_train)

final_model = model_log_gridCV.best_params_
XGB_Best = xgb.XGBClassifier(**final_model)

XGB_Best.fit(X_train_trf, y_train)

pred_result = []

model_pred = XGB_Best.predict(X_test_trf)
pred_result.append(model_pred)