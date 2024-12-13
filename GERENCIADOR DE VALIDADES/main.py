import mysql.connector
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for
import notificação  # Importa o módulo de notificação

app = Flask(__name__, template_folder='templates')

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='gerencia',
        )
        if conexao.is_connected():
            return conexao
    except mysql.connector.Error as err:
        print(f'Erro ao conectar: {err}')
        return None

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Página para adicionar produtos
@app.route('/add', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        codigo_barras = request.form['codigo_barras']
        data_validade = request.form['data_validade']
        data_fabricacao = request.form['data_fabricacao']
        fornecedor = request.form['fornecedor']
        
        # Inserir dados no banco de dados
        conexao = conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = 'INSERT INTO validades (nome, codigo_barras, data_validade, data_fabricacao, fornecedor) VALUES (%s, %s, %s, %s, %s)'
                valores = (nome, codigo_barras, data_validade, data_fabricacao, fornecedor)
                cursor.execute(sql, valores)
                conexao.commit()
                print("Dados inseridos com sucesso!")
                return redirect(url_for('index'))
            except Exception as e:
                print(f"Erro ao executar a operação no banco de dados: {e}")
            finally:
                cursor.close()
                conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")
    
    return render_template('add.html')

# Rota para excluir produto
@app.route('/excluir_produto', methods=['POST'])
def excluir_produto():
    codigo_barras = request.form['codigo_barras']
    
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM validades WHERE codigo_barras = %s', (codigo_barras,))
            conexao.commit()
        except Exception as e:
            print(f"Erro ao excluir o produto: {e}")
        finally:
            cursor.close()
            conexao.close()

    return redirect(url_for('produtos_proximos_validade'))

# Página para listar produtos próximos da validade
@app.route('/validade', methods=['GET'])
def produtos_proximos_validade():
    conexao = conectar_banco()
    produtos = []
    produto = None
    erro = None

    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            data_limite = datetime.now() + timedelta(days=7)
            cursor.execute('SELECT nome, codigo_barras, data_fabricacao, fornecedor, data_validade FROM validades')
            produtos = cursor.fetchall()

            codigo_barras = request.args.get('codigo_barras')
            if codigo_barras:
                cursor.execute('SELECT * FROM validades WHERE codigo_barras = %s', (codigo_barras,))
                produto = cursor.fetchone()
                if not produto:
                    erro = "Produto não encontrado."
        except mysql.connector.Error as e:
            print(f"Erro ao buscar produtos: {e}")
        finally:
            cursor.close()
            conexao.close()

        return render_template('validade.html', produtos=produtos, produto=produto, erro=erro)
    else:
        print("Não foi possível conectar ao banco de dados.")
        return redirect(url_for('index'))

# Buscar produtos por fornecedor
@app.route('/buscar_fornecedor', methods=['GET'])
def buscar_fornecedor():
    fornecedor = request.args.get('fornecedor')
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM validades WHERE fornecedor LIKE %s", (f"%{fornecedor}%",))
            produtos = cursor.fetchall()
            return render_template('validade.html', produtos=produtos)
        except mysql.connector.Error as e:
            print(f"Erro ao buscar fornecedor: {e}")
        finally:
            cursor.close()
            conexao.close()
    else:
        print("Não foi possível conectar ao banco de dados.")
        return redirect(url_for('index'))


if __name__ == "__main__":
    import os
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        notificação.executar_notificacao()  # Executa as notificações automaticamente
    app.run(debug=True)
