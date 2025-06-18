class DecisionMaker:
    @staticmethod
    def generate_recommendations(probabilities):
        """
        Формирование рекомендаций на основе вероятностей
        :param probabilities: массив вероятностей
        :return: список рекомендаций
        """
        recommendations = []
        for prob in probabilities:
            if prob < 0.3:
                rec = {
                    'decision': 'Approved',
                    'risk_level': 'Low',
                    'interest_rate': 'Low (5-7%)',
                    'limit': 'High (up to requested amount)',
                    'probability': prob
                }
            elif prob < 0.7:
                rec = {
                    'decision': 'Approved with conditions',
                    'risk_level': 'Medium',
                    'interest_rate': 'Standard (8-12%)',
                    'limit': 'Moderate (70% of requested)',
                    'probability': prob
                }
            else:
                rec = {
                    'decision': 'Rejected',
                    'risk_level': 'High',
                    'interest_rate': 'N/A',
                    'limit': 'N/A',
                    'probability': prob
                }
            recommendations.append(rec)
        return recommendations
    
    @staticmethod
    def make_decision(model, X):
        """
        Принятие решения о кредитоспособности
        :param model: обученная модель
        :param X: данные для предсказания
        :return: список решений
        """
        probabilities = model.predict(X)
        return DecisionMaker.generate_recommendations(probabilities)