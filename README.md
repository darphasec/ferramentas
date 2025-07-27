 Phishing Simulator Advanced

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-lightgrey.svg)
![License](https://img.shields.io/badge/license-GPLv3-red.svg)

Ferramenta educacional para testes de conscientização em segurança digital

> ⚠️ AVISO LEGAL: Este projeto deve ser usado APENAS para fins educacionais e testes autorizados. Qualquer uso malicioso é expressamente proibido.
📌 Objetivo
Simular cenários de phishing realistas para:
- Treinamento de equipes
- Testes de conscientização
- Pesquisa em segurança cibernética

 🛠️ Instalação

 git clone https://github.com/seu-usuario/phishing-simulator-advanced.git
cd phishing-simulator-advanced

 Estrutura de arquivos (execute no terminal)

 mkdir -p {static/css,templates,uploads,logs}
touch app.py static/css/style.css templates/{base,login,dashboard,checkout}.html
touch requirements.txt README.md WARNING.md .env.sample


# Configurações básicas
app.config.update(
    SECRET_KEY='sua_chave_secreta',
    UPLOAD_FOLDER='caminho/para/uploads',
    WEBHOOK_URL='https://seu-webhook.com'  # Opcional
)



