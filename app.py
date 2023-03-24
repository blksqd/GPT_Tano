from flask import Flask, request, jsonify
from transformers import GPTNeoForCausalLM, GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

# Load GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.strip()

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_input = data.get("user_input")
    if user_input:
        chatbot_response = generate_response(user_input)
        return jsonify({"response": chatbot_response})
    else:
        return jsonify({"error": "No user_input provided."})

if __name__ == '__main__':
    app.run(debug=True)