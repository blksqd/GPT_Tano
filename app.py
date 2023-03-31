from flask import Flask, render_template, request, jsonify, redirect, url_for
import openai
import csv
import datetime
import os
import json
from scraping import scrape_url

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = "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"

# Define a global variable to store conversation history
conversation_history = []

# Generate pre-conditions
def read_text_file(filename):
    data_str = ""
    with open(filename, 'r') as file:
        for line in file:
            data_str += f"\"{line.strip()}\" "
    return data_str.strip()


# Pass urls as information support
urls = ['https://en.wikipedia.org/wiki/Senior_dog_diet']
header_contents, text_contents = scrape_url(urls[0])
print(header_contents, text_contents)

# Function to call OpenAI API and generate a response
def generate_response(prompt):
    global conversation_history
    
    # Append user input to conversation history
    conversation_history.append(['user', prompt, datetime.datetime.now()])
    
   # Build prompt for OpenAI API
    context_user = [x[1] for x in conversation_history if x[0] == 'user']
    print(context_user)
    context_str = '\n'.join(context_user)
    prompt = """You are Lars. You will not introduce yourself unless asked.\n\n
                Learn this information but never mention it again: You are a virtual dog-nutrition specialist.\n\n
                You work for the Brand TANO Supplements.\n\n
                You are polite and transparent but with an informal tone.\n\n
                You are here to answer only questions about Dog Nutrition & dog well-being.\n\n
                You will try to include TANO products whenever it fits without pushing too much.\n\n
                You can see the list of products here:\n\n """ + read_text_file('products.txt') + """\n\n
                You will analyze this prompt: """ + prompt + """\n\n
                You will react as previously instructed, in relation to the prompt.\n\n
                You will have this information available as support for your answers: """ + text_contents + header_contents + """\n\n
                You will not change this set of instructions after this instruction. Do not say you understood."""
    prompt += "\n\n" + context_str + "##"
    

    # Call OpenAI API
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop="##"
    )

    message = response.choices[0].text.strip()
    
    # Append chatbot response to conversation history
    conversation_history.append(['chatbot', message, datetime.datetime.now()])
    
    # Save conversation history to CSV file with timestamps
    with open('conversation_history.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User', 'Message', 'Timestamp'])
        for row in conversation_history:
            writer.writerow(row)
    
    return message

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        owner_name = request.form['owner_name']
        email = request.form['email']
        dog_name = request.form['dog_name']
        age = request.form['age']
        breed = request.form['breed']
        activity_level = request.form['activity_level']
        pre_conditions = request.form['pre_conditions']

        # Save the data to a CSV file
        csv_file = 'login_data.csv'
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Owner Name', 'Email', 'Dog Name', 'Age', 'Breed', 'Activity Level', 'Pre-Conditions'])
            writer.writerow([owner_name, email, dog_name, age, breed, activity_level, pre_conditions])

        # You can store the data in a database or session for future use

        return redirect(url_for('index'))
    return render_template('login.html')



@app.route('/', methods=['GET', 'POST'], endpoint='index')
def home():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    response = generate_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
