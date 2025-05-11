# Bot Discord para RPG

## Descrição
Um bot Discord especializado em auxiliar jogadores e mestres de RPG, desenvolvido para tornar suas sessões mais dinâmicas e organizadas. Com uma interface intuitiva e comandos eficientes, o bot facilita o gerenciamento de combates, rolagens de dados e consultas de regras.

### 🎲 Principais Funcionalidades

- **Sistema de Dados Avançado**
  - Rolagens no formato tradicional (!d20, !3d6+1)
  - Suporte a múltiplos dados e modificadores
  - Resultados formatados de forma clara e organizada

- **Gerenciamento de Iniciativa**
  - Controle preciso da ordem de combate
  - Adição e remoção de participantes
  - Visualização clara da ordem dos turnos

- **Biblioteca de Magias**
  - Consulta rápida de magias
  - Detalhes completos incluindo componentes, duração e efeitos
  - Filtros por nível, escola e tipo

- **Catálogo de Itens**
  - Informações detalhadas sobre equipamentos
  - Preços, peso e propriedades
  - Fácil consulta por nome ou tipo

- **Referência de Condições**
  - Descrições claras de condições de D&D
  - Efeitos e duração
  - Regras específicas para cada condição

### 🎯 Benefícios

- **Eficiência**: Automatiza tarefas repetitivas, permitindo que você foque na narrativa
- **Organização**: Mantém o combate e as rolagens organizados e claros
- **Acessibilidade**: Interface intuitiva com comandos slash (/) para fácil acesso
- **Confiabilidade**: Resultados precisos e consistentes para todas as rolagens

### 🎮 Como Usar

O bot utiliza comandos slash (/) para uma experiência mais intuitiva:
- `/iniciativa` - Gerencia a ordem de combate
- `/rolar` - Realiza rolagens de dados
- `/magia` - Consulta informações sobre magias
- `/item` - Busca detalhes de equipamentos
- `/condicao` - Mostra informações sobre condições

Para rolagens rápidas, use o formato tradicional:
- `!d20` - Rola um d20
- `!3d6+1` - Rola três d6 e adiciona 1
- `!2d8-2` - Rola dois d8 e subtrai 2

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
