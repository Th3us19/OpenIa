import openai
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

load_dotenv()
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

mensagens = [{
    "role": "system",
    "content": f"Você é um assistente útil. O ano atual é 2025. Hoje é {datetime.now().strftime('%d/%m/%Y')}."
}]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    mensagens.append({"role": "user", "content": user_message})
    
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=mensagens,
        max_tokens=1000,
        temperature=0,
        stream=False
    )
    
    texto_completo = resposta.choices[0].message.content
    mensagens.append({"role": "assistant", "content": texto_completo})
    
    return jsonify({'response': texto_completo})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)