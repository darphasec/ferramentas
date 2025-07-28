


Ferramenta educacional para testes de conscientização em segurança digital

 AVISO : Este projeto deve ser usado APENAS para fins educacionais e testes autorizados. Qualquer uso malicioso é expressamente proibido.

 Objetivo
Simular cenário de phishing DE UMA LOJA online DE COURSus digitais de IT .........
- Treinamento de equipes
- Testes de conscientização
- Pesquisa em segurança cibernética

Instalação

git clone ...............
 
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



