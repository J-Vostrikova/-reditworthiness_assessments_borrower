
### 4. `src/data_processing.py`

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import joblib

class DataProcessor:
    def __init__(self):
        self.preprocessor = None
        self.categorical_features = [
            'checking_account', 'credit_history', 'purpose', 'savings_account',
            'employment', 'personal_status', 'other_debtors', 'property',
            'other_installment_plans', 'housing', 'job', 'telephone', 'foreign_worker'
        ]
        self.numeric_features = [
            'duration', 'credit_amount', 'installment_rate', 'residence_since',
            'age', 'existing_credits', 'people_liable'
        ]
    
    def load_data(self, path):
        """Загрузка данных из CSV файла"""
        data = pd.read_csv(path)
        if 'target' in data.columns:
            data['target'] = data['target'].map({1: 0, 2: 1})
        return data
    
    def preprocess_data(self, data):
        """Предобработка данных"""
        # Удаление дубликатов
        data = data.drop_duplicates()
        
        # Разделение на признаки и целевую переменную
        if 'target' in data.columns:
            X = data.drop('target', axis=1)
            y = data['target']
        else:
            X = data
            y = None
        
        # Создание и обучение препроцессора
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), self.numeric_features),
                ('cat', OneHotEncoder(drop='first'), self.categorical_features)
            ])
        
        X_processed = self.preprocessor.fit_transform(X)
        return X_processed, y
    
    def split_data(self, X, y, test_size=0.2):
        """Разделение данных на обучающую и тестовую выборки"""
        return train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y)
    
    def save_preprocessor(self, path):
        """Сохранение препроцессора"""
        if self.preprocessor:
            joblib.dump(self.preprocessor, path)
    
    def load_preprocessor(self, path):
        """Загрузка препроцессора"""
        self.preprocessor = joblib.load(path)
        return self.preprocessor