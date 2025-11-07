from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Модель zero-shot (BART, легкая для CPU)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    text = data.get('text', '')
    candidate_labels = data.get('labels', [])  # Пример: ["joy", "sadness", "погода", "работа"]

    if not text or not candidate_labels:
        return jsonify({"error": "Missing text or labels"}), 400

    result = classifier(text, candidate_labels, multi_label=True)
    # Возвращает топ-лейблы (эмоция + топик)
    top_emotion = result['labels'][0] if result['labels'] else None
    top_topic = result['labels'][1] if len(result['labels']) > 1 else None

    return jsonify({
        "emotion": top_emotion,
        "topic": top_topic,
        "scores": result['scores']
    })

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
