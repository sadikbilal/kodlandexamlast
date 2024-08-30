from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'gizli_anahtar'

questions = [
    {"question": "Konvolüsyonel katmanın amacı nedir?", "answers": ["Özellik çıkarma", "Veri artırma", "Havuzlama", "Normalizasyon"], "correct": "Özellik çıkarma"},
    {"question": "CNN'in açılımı nedir?", "answers": ["Konvolüsyonel Sinir Ağı", "Merkezi Sinir Ağı", "Hesaplamalı Sinir Ağı", "Kodlanmış Sinir Ağı"], "correct": "Konvolüsyonel Sinir Ağı"},
    {"question": "Bir görüntünün uzaysal boyutunu azaltmak için hangi teknik kullanılır?", "answers": ["Konvolüsyon", "Dolgu", "Havuzlama", "ReLU"], "correct": "Havuzlama"},
    {"question": "Bir sinir ağındaki aktivasyon fonksiyonunun rolü nedir?", "answers": ["Nöronları aktifleştirmek", "Doğrusal olmayanlık eklemek", "Veriyi normalize etmek", "Ağırlıkları optimize etmek"], "correct": "Doğrusal olmayanlık eklemek"},
]

def calculate_percentage(score, total_questions):
    percentage = (score / total_questions) * 100
    if percentage == 100:
        return "100%"
    elif percentage >= 75:
        return "75%"
    elif percentage >= 50:
        return "50%"
    elif percentage >= 25:
        return "25%"
    else:
        return "0%"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        score = 0
        for i, question in enumerate(questions):
            selected_answer = request.form.get(f'soru-{i}')
            if selected_answer == question['correct']:
                score += 1
        
        total_questions = len(questions)
        percentage_score = calculate_percentage(score, total_questions)
        
        session['score'] = percentage_score
        session['high_score'] = max(session.get('high_score', "0%"), percentage_score)
        return redirect(url_for('result'))

    return render_template('index.html', questions=questions)

@app.route('/result')
def result():
    score = session.get('score', "0%")
    high_score = session.get('high_score', "0%")
    return render_template('result.html', score=score, high_score=high_score)

@app.route('/reset')
def reset():
    session.pop('score', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

