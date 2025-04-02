# Sistema de Gerenciamento de Tickets

## Descrição
Este é um sistema de gerenciamento de tickets desenvolvido em Django. Ele permite que usuários cadastrem tickets, alterem seus status e acompanhem o tempo desde a criação. O sistema também inclui um chat em tempo real para comunicação eficiente entre os usuários.

## Funcionalidades
- **Cadastro e autenticação de usuários**
- **Criação de tickets** com título, descrição e status
- **Alterar status** dos tickets
- **Contador de tempo** em minutos para cada ticket
- **Chat em tempo real** para discussão sobre os tickets

## Tecnologias Utilizadas
- **Python 3
- **Django** (Back-end)
- **Django Channels** (WebSockets para chat em tempo real)
- **Bootstrap** (Front-end)
- **SQLite** (Banco de dados padrão, pode ser alterado para PostgreSQL ou MySQL)

## Requisitos
Antes de iniciar, instale os seguintes pacotes:
```sh
pip install -r requirements.txt
```

## Configuração e Execução
1. Clone o repositório:
```sh
git clone https://github.com/leandrofratel/Django_Tickets_Chat.git
```
2. Navegue até a pasta do projeto:
```sh
cd sistema
```
3. Configure o banco de dados:
```sh
python manage.py migrate
```
4. Crie um superusuário (Para criar as salas de bate-papo):
```sh
python manage.py createsuperuser
```
5. Inicie o servidor:
```sh
python manage.py runserver
```
6. Acesse o sistema em [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Como Usar
- **Cadastro/Login**: Usuários devem se cadastrar e fazer login para acessar o sistema.
- **Gerenciamento de Tickets**: Criar, editar e alterar status dos tickets.
- **Chat em Tempo Real**: Acessar salas de bate-papo vinculadas aos tickets.

## Licença
Este projeto está sob a licença MIT. Sinta-se livre para usá-lo e modificá-lo conforme necessário.

---
Desenvolvido por Leandro Fratel.
---