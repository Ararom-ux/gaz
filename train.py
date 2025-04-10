import numpy as np
from sklearn.neural_network import MLPClassifier
import joblib
import random
from sklearn.model_selection import train_test_split  # Для разделения данных

# Генерация случайных обучающих данных
def generate_training_data(num_samples=1000):
    X = []
    y = []
    
    # Возможные значения
    zones = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    wind_speeds = [0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]  # Ветер от 0.3 до 5.0 м/с
    gas_volumes = [5, 10, 20, 30, 50, 100, 150, 200, 300, 500]  # Объем газа в м³
    explosion_risks = ["Низкая", "Средняя", "Высокая"]
    
    # Генерируем заданное количество случайных случаев
    for _ in range(num_samples):
        zone = random.choice(zones)
        wind_speed = random.choice(wind_speeds)
        gas_volume = random.choice(gas_volumes)
        
        # Определяем риск взрыва на основе объема газа
        if gas_volume <= 20:
            risk_level = "Низкая"
        elif gas_volume <= 100:
            risk_level = "Средняя"
        else:
            risk_level = "Высокая"
        
        # Риск для нейросети: Низкий (0), Средний (1), Высокий (2)
        risk_level_numeric = {"Низкая": 0, "Средняя": 1, "Высокая": 2}[risk_level]
        
        # Объем газа, скорость ветра, риск взрыва и зона
        X.append([gas_volume, wind_speed, risk_level_numeric, zone])
        
        # Определяем целевой класс
        if risk_level_numeric == 2:  # Высокий риск взрыва -> экстренная мера (эвакуация или взрыв)
            y.append(1)
        else:  # Средний или низкий риск -> нет экстренной меры
            y.append(0)
    
    return np.array(X), np.array(y)

# Генерация данных
X, y = generate_training_data(num_samples=1000)

# Разделяем данные на обучающие и тестовые (80% на обучение, 20% на тест)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создаем и обучаем модель нейросети
model = MLPClassifier(hidden_layer_sizes=(20,), max_iter=2000, tol=1e-4, learning_rate_init=0.001)
model.fit(X_train, y_train)

# Сохраняем обученную модель в файл
joblib.dump(model, 'trained_model.pkl')

# Оценка точности модели на тестовых данных
accuracy = model.score(X_test, y_test)
print(f"Точность модели на тестовых данных: {accuracy * 100:.2f}%")

print("Модель успешно обучена и сохранена в файл 'trained_model.pkl'.")