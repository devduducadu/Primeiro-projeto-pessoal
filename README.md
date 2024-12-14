# Primeiro projeto pessoal
 HISTÓRIA: A ideia desse projeto surgiu quando eu estava trabalhando em um mercado, em que o processo de gerenciar a validade era feita manualmente com papel e caneta, sendo assim, o processo era muito cansativo e lento...

 DESCRIÇÃO: O que o projeto faz?
Gerenciamento de Validades: Monitora produtos cadastrados e identifica aqueles que estão próximos de vencer (dentro de 7 dias).
Notificações por E-mail: Envia e-mails automáticos com os produtos que precisam de atenção.
Execução Automática: O sistema roda diariamente, duas vezes ao dia, nos horários programados (8h e 20h), sem intervenção manual.

Ferramentas, Tecnologias e Bibliotecas Utilizadas:
Google Sheets API: É Usada para armazenar e gerenciar os dados dos produtos de forma online e acessível.

MySQL: Banco de dados local utilizado para registrar e consultar as informações de forma eficiente.

Flask: Framework web utilizado no início do projeto para criar e testar a interface de gerenciamento.

Google Apps Script: Ferramenta responsável pela automação e integração com o Google Sheets e Gmail, além do agendamento de tarefas.

Gmail API: Implementada para o envio das notificações por e-mail diretamente da aplicação.

smtplib: Para envio de e-mails.

datetime: Para trabalhar com datas e calcular os prazos.

mysql-connector-python: Para conexão com o banco de dados MySQL.

