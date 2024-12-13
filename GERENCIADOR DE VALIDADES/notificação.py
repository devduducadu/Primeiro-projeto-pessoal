from main import conectar_banco  # Importa a função de conexão ao banco
from datetime import datetime, timedelta
import smtplib
import email.message
import mysql.connector

def executar_notificacao():
    try:
        # Conectar ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='gerencia',
        )
        
        if conexao.is_connected():
            print("Conexão com o banco de dados estabelecida para notificações.")

            # Definir o período de notificação (7 dias a partir de hoje)
            data_atual = datetime.now()
            data_limite = data_atual + timedelta(days=7)

            cursor = conexao.cursor(dictionary=True)

            # Buscar produtos que estão próximos da validade
            query = """
                SELECT nome, codigo_barras, data_fabricacao, data_validade, fornecedor
                FROM validades
                WHERE data_validade BETWEEN %s AND %s
            """
            cursor.execute(query, (data_atual, data_limite))
            produtos = cursor.fetchall()

            # Exibir as notificações no console
            if produtos:
                print("==== PRODUTOS PRÓXIMOS DA VALIDADE ====")
                for produto in produtos:
                    print(
                        f"Produto: {produto['nome']} | Código de Barras: {produto['codigo_barras']} | "
                        f"Data de Fabricação: {produto['data_fabricacao']} | Validade: {produto['data_validade'].strftime('%d/%m/%Y')} | Fornecedor: {produto['fornecedor']}"
                    )

                # Enviar e-mail com os produtos próximos da validade
                enviar_email(produtos)
            else:
                print("Nenhum produto próximo da validade encontrado.")

            # Fechar conexões
            cursor.close()
            conexao.close()

    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco para notificações: {e}")


# Função para obter os produtos que estão a 7 dias de vencer
def obter_produtos_para_notificacao():
    hoje = datetime.now()
    data_limite = hoje + timedelta(days=7)  # Define o intervalo de produtos próximos da validade

    try:
        conexao = conectar_banco()  # Usa a função importada do main.py
        cursor = conexao.cursor(dictionary=True)  # Retorna resultados como dicionários

        # Consulta SQL para buscar os produtos que atendem ao critério de validade
        cursor.execute("""
            SELECT nome, codigo_barras, data_fabricacao, fornecedor, data_validade
            FROM validades
            WHERE data_validade BETWEEN %s AND %s
        """, (hoje, data_limite))

        produtos = cursor.fetchall()  # Recupera todos os produtos encontrados
        cursor.close()
        conexao.close()
        return produtos
    except Exception as err:
        print(f"Erro ao obter os produtos: {err}")
        return []


# Função para enviar e-mail com os produtos próximos da validade
def enviar_email(produtos):
    if not produtos:
        print("Nenhum produto para notificação.")
        return

    # Monta a mensagem do e-mail com base nos produtos
    corpo_email = "<h2>Produtos próximos da validade:</h2>"
    for produto in produtos:
        corpo_email += f"""
        <p>
        Nome: {produto['nome']}<br>
        Código de Barras: {produto['codigo_barras']}<br>
        Data de Fabricação: {produto['data_fabricacao']}<br>
        Fornecedor: {produto['fornecedor']}<br>
        Data de Validade: {produto['data_validade']}
        </p>
        """

    try:
        msg = email.message.Message()
        msg['Subject'] = "Produtos entrando em vencimento hoje"
        msg['from'] = "duducard495@gmail.com"  # Seu e-mail
        msg['to'] = "duducard495@gmail.com"    # Destinatário (pode ser o mesmo seu ou outro)
        password = "cbkj vlhz oweq lsyo"  # Senha de app do seu Gmail (não sua senha normal)

        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com:587')
        s.starttls()
        s.login(msg['from'], password)
        s.sendmail(msg['from'], [msg['to']], msg.as_string().encode('utf-8'))
        print('E-mail enviado com sucesso.')
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


# Execução principal
if __name__ == "__main__":
    # Executa a notificação para os produtos próximos da validade e envia o e-mail
    executar_notificacao()
