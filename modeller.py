import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from xgboost import XGBRegressor

import warnings
warnings.filterwarnings("ignore")

# Veriyi oku
df = pd.read_csv("data_yolu")

# Gerekli sütunları seç ve temizle
df = df[['Description', 'Category', 'Reviews', 'Installs', 'Type', 'Price', 'Content Rating', 'Rating']]
df.dropna(inplace=True)
df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df['Installs'] = df['Installs'].replace('[\+,]', '', regex=True).astype(float)

# Ekstra özellik
df['Description_length'] = df['Description'].apply(lambda x: len(str(x).split()))

# Özellikler ve hedef değişken
X = df[['Description', 'Category', 'Reviews', 'Installs', 'Type', 'Price', 'Content Rating']]
y = df['Rating']

# Eğitim/test ayrımı
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Dönüştürücüler
text_features = 'Description'
categorical_features = ['Category', 'Type', 'Content Rating']
numeric_features = ['Reviews', 'Installs', 'Price']

# Ön işleme
preprocessor = ColumnTransformer([
    ('text', TfidfVectorizer(max_features=3000), text_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
    ('num', StandardScaler(), numeric_features)
])

# Kullanılacak modeller
models = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(),
    "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
    "GradientBoosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
    "XGBoost": XGBRegressor(n_estimators=100, random_state=42, verbosity=0)
}

# Performans metriklerini sakla
results = []

for name, model in models.items():
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', model)
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    y_train_pred = pipeline.predict(X_train)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    r2_train = r2_score(y_train, y_train_pred)
    adj_r2 = 1 - (1 - r2) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)

    results.append({
        'Model': name,
        'RMSE': rmse,
        'MAE': mae,
        'R2': r2,
        'Adjusted R2': adj_r2,
        'Train R2': r2_train,
        'Test R2': r2,
        'Overfitting Risk': 'Overfitting' if (r2_train - r2 > 0.1) else ('Underfitting' if r2 < 0.3 else 'Normal')
    })

# Sonuçları DataFrame olarak göster
results_df = pd.DataFrame(results)
print(results_df)

# Performans metriklerini çiz
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
sns.barplot(x='Model', y='RMSE', data=results_df)
plt.title('Model Bazlı RMSE Karşılaştırması')
plt.xticks(rotation=45)

plt.subplot(1, 2, 2)
sns.barplot(x='Model', y='R2', data=results_df)
plt.title('Model Bazlı R2 Skoru')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Overfitting/Underfitting durumları
plt.figure(figsize=(8, 6))
sns.barplot(x='Model', y='Train R2', data=results_df, label='Train', color='blue')
sns.barplot(x='Model', y='Test R2', data=results_df, label='Test', color='orange')
plt.title('Train vs Test R2 (Overfitting / Underfitting Analizi)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()