Sobre o Projeto
Este projeto é uma ferramenta educacional que simula uma loja digital falsa que contem cursos online de it
ojectivo: para treinamento em conscientização sobre ataques de phishing.  
Ele permite criar um ambiente de teste onde usuários podem ser expostos a práticas comuns de phishing, sem risco real, visando ensinar como identificar e evitar golpes.

 Funcionalidades
- Página de login falso para capturar credenciais .
- Página de checkout falso simulando roubo de dados de cartão.
- Upload de documentos para o escalamento de vazamento de dados.
- Logs detalhados de todas as interações.
- Modo stealth para execução silenciosa.
- Suporte a Webhook para envio dos dados simulados.

- ❗Uso estritamente educacional  
Este projeto deve ser utilizado apenas em ambientes de teste controlados e com autorização.  
 O uso indevido para fins maliciosos é ilegal e de total responsabilidade do usuário.

Instalação
Clone o repositório

Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Instale as dependências
pip install -r requirements.txt

 Iniciar o servidor
 python3 simulador.py  --port 5000 (a porta que desejar)

