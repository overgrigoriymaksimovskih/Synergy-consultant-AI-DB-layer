from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Модель zero-shot (BART, легкая для CPU). Если точность низкая, рассмотрите дообучение или другую модель (например, для эмоций - sentiment-analysis pipeline).
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Определяем эмоции и топики явно (можно вынести в конфиг). Добавьте больше, если нужно (например, "anger" для эмоций).
EMOTIONS = ["joy", "sadness", "anger", "fear", "disgust", "surprise", "neutral"]
TOPICS = ["погода", "работа", "семья", "друзья", "здоровье", "спорт", "финансы", "технологии", "развлечения", "отношения", "чувства", "общее"]

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    text = data.get('text', '')
    candidate_labels = data.get('labels', [])  # Пример: ["joy", "sadness", "погода", "работа"]

    if not text or not candidate_labels:
        return jsonify({"error": "Missing text or labels"}), 400

    result = classifier(text, candidate_labels, multi_label=True)

    # Разделяем результаты на эмоции и топики
    labels = result['labels']
    scores = result['scores']

    # Ищем топ эмоцию (максимальный score среди эмоций)
    top_emotion = None
    top_emotion_score = 0.0
    for label, score in zip(labels, scores):
        if label in EMOTIONS and score > top_emotion_score:
            top_emotion = label
            top_emotion_score = score

    # Ищем топ топик (максимальный score среди топиков)
    top_topic = None
    top_topic_score = 0.0
    for label, score in zip(labels, scores):
        if label in TOPICS and score > top_topic_score:
            top_topic = label
            top_topic_score = score

    # Если топ не найден, устанавливаем "unknown" (для robustness)
    if not top_emotion:
        top_emotion = "unknown"
    if not top_topic:
        top_topic = "unknown"

    # Возвращаем в формате, соответствующем вашему Java-клиенту (списки, как в предыдущих логах)
    return jsonify({
        "emotions": [top_emotion],
        "topics": [top_topic],
        "scores": result['scores']  # Оставляем полные scores для отладки
    })

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
