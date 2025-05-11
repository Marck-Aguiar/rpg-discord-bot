# Nome do Seu Bot

## Descrição
Uma breve descrição do que seu bot faz.

## Configuração
1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
3. Ative o ambiente virtual:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```
   DISCORD_TOKEN=seu_token_aqui
   ```

## Executando o Bot
```bash
python main.py
```

## Dependências
- discord.py
- python-dotenv
