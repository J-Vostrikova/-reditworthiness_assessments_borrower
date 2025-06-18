from data_processing import DataProcessor
from model import CreditScoringModel
from decision_logic import DecisionMaker
from database import DecisionDatabase
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

def main():
    # Инициализация компонентов
    data_processor = DataProcessor()
    model = CreditScoringModel()
    db = DecisionDatabase()
    
    try:
        # 1. Загрузка и предобработка данных
        print("Загрузка и предобработка данных...")
        data = data_processor.load_data('data/german_credit.csv')
        X, y = data_processor.preprocess_data(data)
        X_train, X_test, y_train, y_test = data_processor.split_data(X, y)
        
        # 2. Обучение модели
        print("\nОбучение модели...")
        model.build_model(X_train.shape[1])
        model.train(X_train, y_train)
        
        # 3. Оценка модели
        print("\nОценка модели на тестовых данных...")
        test_loss, test_acc, test_auc = model.evaluate(X_test, y_test)
        print(f"Test Accuracy: {test_acc:.4f}, Test AUC: {test_auc:.4f}")
        
        # 4. Визуализация результатов
        y_pred = (model.predict(X_test) > 0.5).astype(int)
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Матрица ошибок
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
        plt.show()
        
        # 5. Пример работы с новыми данными
        print("\nПример работы с новыми данными...")
        sample_data = data.sample(1).drop('target', axis=1)
        X_sample = data_processor.preprocessor.transform(sample_data)
        
        decisions = DecisionMaker.make_decision(model, X_sample)
        
        for i, decision in enumerate(decisions):
            print(f"\nРешение для клиента #{i+1}:")
            print(f"Вероятность погашения: {decision['probability']:.2%}")
            print(f"Решение: {decision['decision']}")
            print(f"Уровень риска: {decision['risk_level']}")
            print(f"Процентная ставка: {decision['interest_rate']}")
            print(f"Кредитный лимит: {decision['limit']}")
            
            # Сохранение решения в БД
            db.store_decision(sample_data.iloc[i].to_dict(), decision)
        
        # Сохранение артефактов
        print("\nСохранение модели и препроцессора...")
        model.save_model('models/credit_model.h5')
        data_processor.save_preprocessor('models/preprocessor.pkl')
        
    finally:
        db.close()
        print("\nРабота системы завершена.")

if __name__ == "__main__":
    main()