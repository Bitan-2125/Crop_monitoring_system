"""
Run this script once to retrain the crop recommendation model
with your current scikit-learn version.
Usage: python retrain_model.py  (from inside the app/ folder)
"""
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('../Data-processed/crop_recommendation.csv')

X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

model = RandomForestClassifier(n_estimators=20, random_state=0)
model.fit(X, y)

with open('models/RandomForest.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model retrained and saved to models/RandomForest.pkl")
