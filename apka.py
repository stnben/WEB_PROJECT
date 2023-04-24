
import os
import openai
import time
from flask import render_template
from dotenv import load_dotenv
from flask import Flask, request, jsonify

user_preferences = {}

app = Flask(__name__)

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY



@app.route('/api/handle_message', methods=['POST'])
def handle_message():
    print(request.data)
    print("Entered handle_message")
    try:
        data = request.get_json(force=True)
        print("Received data:", data)
        user_id = data['user_id']
        user_input = data['input']

        user_prefs = user_preferences.get(user_id, {})

        response = process_input(user_input, user_prefs.get('position'), user_prefs.get('num_questions'), user_prefs.get('difficulty'), user_prefs.get('category'))

        return jsonify({'response': response})
    except Exception as e:
        print("Error in handle_message:", e)
        return jsonify({"error": str(e)}), 400


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/set_preferences', methods=['POST'])
def set_preferences():
    try:
        data = request.get_json(force=True)
        user_id = data['user_id']
        user_name = data['userName']
        interview_duration = data['interviewDuration']
        position = data['position']
        num_questions = data['num_questions']
        difficulty = data['difficulty']
        category = data['category']

        user_preferences[user_id] = {
            'user_name': user_name,
            'interview_duration': interview_duration,
            'position': position,
            'num_questions': num_questions,
            'difficulty': difficulty,
            'category': category,
        }

        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})




def interview():
    data = request.get_json()
    user_input = data['input']
    position = data['position']
    num_questions = data['num_questions']
    difficulty = data['difficulty']
    category = data['category']

    response = process_input(user_input, position, num_questions, difficulty, category)

    return jsonify({'response': response})

def process_input(user_input, position, num_questions, difficulty, category):
    response = generate_question(user_input, position, num_questions, difficulty, category)
    return response

def generate_question(prompt, job_position, num_questions, difficulty, category):
    prompt = f"Continue an interview for the position of {job_position} with the following answer: \"{prompt}\". Ask a relevant {difficulty} difficulty question."

    if category is not None:
        prompt += f" The question should be related to {category}."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                'role': 'system',
                'content': f"You are a helpful assistant that helps users practice for job interviews."
            }, {
                'role': 'user',
                'content': prompt
            }],
            max_tokens=100,
            n=1,
            temperature=1.0,
        )
    except openai.error.RateLimitError as e:
        print("Rate limit exceeded. Retrying in 60 seconds...")
        time.sleep(60)
        return generate_question(prompt, job_position, num_questions, difficulty, category)

    time.sleep(1)

    question = response.choices[0].message['content'].strip()
    return question.lstrip('0123456789. ')

if __name__ == '__main__':
    app.run(debug=True)

