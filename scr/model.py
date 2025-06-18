from tensorflow import keras
from tensorflow.keras import layers, callbacks
import matplotlib.pyplot as plt

class CreditScoringModel:
    def __init__(self):
        self.model = None
    
    def build_model(self, input_shape):
        """Построение архитектуры модели"""
        self.model = keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(input_shape,)),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(32, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(1, activation='sigmoid')
        ])
        
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.AUC(name='auc')]
        )
        
        return self.model
    
    def train(self, X_train, y_train, validation_split=0.2, epochs=100, batch_size=32):
        """Обучение модели"""
        early_stopping = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6
        )
        
        history = self.model.fit(
            X_train, y_train,
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        self._plot_training_history(history)
        return history
    
    def _plot_training_history(self, history):
        """Визуализация процесса обучения"""
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Train Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Accuracy over epochs')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Loss over epochs')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend()
        
        plt.tight_layout()
        plt.show()
    
    def evaluate(self, X_test, y_test):
        """Оценка модели на тестовых данных"""
        return self.model.evaluate(X_test, y_test, verbose=0)
    
    def predict(self, X):
        """Предсказание вероятностей"""
        return self.model.predict(X).flatten()
    
    def save_model(self, path):
        """Сохранение модели"""
        self.model.save(path)
    
    def load_model(self, path):
        """Загрузка модели"""
        self.model = keras.models.load_model(path)
        return self.model