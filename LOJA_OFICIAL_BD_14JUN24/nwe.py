import tkinter as tk
from tkinter import messagebox
import mysql.connector
import datetime

# Configuração da conexão com o banco de dados
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'solocampo'
}

# Função para validar CPF
def valida(cpf):
    return len(cpf) == 11

class Usuario:
    def __init__(self, nome, apelido, senha, rg, cpf, telefone):
        self.nome = nome
        self.apelido = apelido
        self.senha = senha
        self.email = f"{nome}.{apelido}@gmail.com"
        self.rg = rg
        self.cpf = cpf
        self.telefone = telefone

    def alterar_senha(self, nova_senha):
        self.senha = nova_senha
        messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")

class Cliente(Usuario):
    def __init__(self, nome, rg, cpf, telefone, apelido, senha, endereco):
        super().__init__(nome, apelido, senha, rg, cpf, telefone)
        self.endereco = endereco

    def alterar_endereco(self, novo_endereco):
        self.endereco = novo_endereco
        messagebox.showinfo("Sucesso", "Endereço alterado com sucesso!")

    def salvar_bd(self):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nome, rg, cpf, telefone, apelido, senha, endereco) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (self.nome, self.rg, self.cpf, self.telefone, self.apelido, self.senha, self.endereco))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso no banco de dados!")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

class Funcionario(Usuario):
    def __init__(self, nome, apelido, senha, cargo, rg, cpf, telefone):
        super().__init__(nome, apelido, senha, rg, cpf, telefone)
        self.cargo = cargo

    def salvar_bd(self):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO funcionarios (nome, apelido, senha, cargo, rg, cpf, telefone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (self.nome, self.apelido, self.senha, self.cargo, self.rg, self.cpf, self.telefone))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso no banco de dados!")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

class Produto:
    def __init__(self, id_produto, nome, preco, descricao, tipo, marca, categoria, quantidade):
        self.id_produto = id_produto
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.tipo = tipo
        self.marca = marca
        self.categoria = categoria
        self.quantidade = quantidade

    def exibir_detalhes(self):
        return f"Produto: {self.nome}, Preço: R${self.preco:.2f}, Quantidade disponível: {self.quantidade}, Descrição: {self.descricao}, Id produto: {self.id_produto}"

    def salvar_bd(self):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO produtos (id_produto, nome, preco, descricao, tipo, marca, categoria, quantidade) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (self.id_produto, self.nome, self.preco, self.descricao, self.tipo, self.marca, self.categoria, self.quantidade))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso no banco de dados!")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

    @staticmethod
    def listar_produtos():
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produtos")
            produtos = cursor.fetchall()
            cursor.close()
            conn.close()
            return produtos
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")
            return []

    @staticmethod
    def excluir_produto(nome):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE nome = %s", (nome,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", f"Produto {nome} excluído com sucesso do banco de dados!")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

class Pedido:
    def __init__(self):
        self.produtos = []
        self.valor_total = 0
        self.forma_pagamento = None

    def adicionar_produto(self, produto, quantidade):
        if produto.quantidade >= quantidade:
            self.produtos.append((produto, quantidade))
            self.valor_total += produto.preco * quantidade
            produto.quantidade -= quantidade
            messagebox.showinfo("Produto Adicionado",
                                f"{quantidade} unidade(s) do produto {produto.nome} adicionado(s) ao pedido. Valor total: R${self.valor_total:.2f}\nQuantidade restante do produto {produto.nome}: {produto.quantidade}")
        else:
            messagebox.showwarning("Quantidade Insuficiente",
                                   f"Quantidade insuficiente do produto {produto.nome}. Disponível: {produto.quantidade}")

    def selecionar_forma_pagamento(self, forma):
        self.forma_pagamento = forma

    def realizar_pagamento(self):
        if not self.produtos or not self.forma_pagamento:
            messagebox.showwarning("Erro",
                                   "Por favor, adicione produtos ao pedido e selecione a forma de pagamento antes de realizar o pagamento.")
        else:
            messagebox.showinfo("Pagamento", f"Realizando pagamento via {self.forma_pagamento}...")
            messagebox.showinfo("Sucesso", f"Pagamento de R${self.valor_total:.2f} realizado com sucesso!")
            self.produtos.clear()
            self.valor_total = 0
            self.forma_pagamento = None

clientes = []
funcionarios = []
produtos = []

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WEB TECHNOMUSIC")
        self.geometry("500x500")
        self.usuario_logado = None
        self.pedido_atual = None
        self.create_widgets()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_widgets(self):
        tk.Label(self, text="Bem-vindo à WEB TECHNOMUSIC!").pack(pady=10)
        tk.Button(self, text="Login", command=self.tela_login).pack(pady=5)
        tk.Button(self, text="Cadastrar Funcionário", command=self.tela_cadastro_funcionario).pack(pady=5)
        tk.Button(self, text="Cadastrar Cliente", command=self.tela_cadastro_cliente).pack(pady=5)
        tk.Button(self, text="Buscar Produto", command=self.tela_buscar_produto).pack(pady=5)
        tk.Button(self, text="Listar Produtos", command=self.tela_listar_produtos).pack(pady=5)
        tk.Button(self, text="Sair", command=self.quit).pack(pady=5)

    def tela_login(self):
        self.clear_widgets()
        tk.Label(self, text="Login").pack(pady=10)
        tk.Label(self, text="Apelido").pack()
        apelido_entry = tk.Entry(self)
        apelido_entry.pack()
        tk.Label(self, text="Senha").pack()
        senha_entry = tk.Entry(self, show="*")
        senha_entry.pack()

        def realizar_login():
            apelido = apelido_entry.get()
            senha = senha_entry.get()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM clientes WHERE apelido = %s AND senha = %s", (apelido, senha))
                cliente = cursor.fetchone()
                if cliente:
                    self.usuario_logado = Cliente(cliente[1], cliente[2], cliente[3], cliente[4], cliente[5], cliente[6], cliente[7])
                    self.tela_principal_cliente()
                    return
                cursor.execute("SELECT * FROM funcionarios WHERE apelido = %s AND senha = %s", (apelido, senha))
                funcionario = cursor.fetchone()
                if funcionario.apelido == apelido and funcionario.senha == senha:
                    self.tela_principal_funcionario()
                    return
                messagebox.showerror("Erro", "Apelido ou senha incorretos!")
                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

        tk.Button(self, text="Login", command=realizar_login).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.create_widgets).pack(pady=5)

    def tela_cadastro_funcionario(self):
        self.clear_widgets()
        tk.Label(self, text="Cadastro de Funcionário").pack(pady=10)
        tk.Label(self, text="Nome").pack()
        nome_entry = tk.Entry(self)
        nome_entry.pack()
        tk.Label(self, text="Apelido").pack()
        apelido_entry = tk.Entry(self)
        apelido_entry.pack()
        tk.Label(self, text="Senha").pack()
        senha_entry = tk.Entry(self, show="*")
        senha_entry.pack()
        tk.Label(self, text="Cargo").pack()
        cargo_entry = tk.Entry(self)
        cargo_entry.pack()
        tk.Label(self, text="RG").pack()
        rg_entry = tk.Entry(self)
        rg_entry.pack()
        tk.Label(self, text="CPF").pack()
        cpf_entry = tk.Entry(self)
        cpf_entry.pack()
        tk.Label(self, text="Telefone").pack()
        telefone_entry = tk.Entry(self)
        telefone_entry.pack()

        def cadastrar_funcionario():
            nome = nome_entry.get()
            apelido = apelido_entry.get()
            senha = senha_entry.get()
            cargo = cargo_entry.get()
            rg = rg_entry.get()
            cpf = cpf_entry.get()
            telefone = telefone_entry.get()
            if not nome or not apelido or not senha or not cargo or not rg or not cpf or not telefone:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            funcionario = Funcionario(nome, apelido, senha, cargo, rg, cpf, telefone)
            funcionario.salvar_bd()

        tk.Button(self, text="Cadastrar", command=cadastrar_funcionario).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.create_widgets).pack(pady=5)

    def tela_cadastro_cliente(self):
        self.clear_widgets()
        tk.Label(self, text="Cadastro de Cliente").pack(pady=10)
        tk.Label(self, text="Nome").pack()
        nome_entry = tk.Entry(self)
        nome_entry.pack()
        tk.Label(self, text="Apelido").pack()
        apelido_entry = tk.Entry(self)
        apelido_entry.pack()
        tk.Label(self, text="Senha").pack()
        senha_entry = tk.Entry(self, show="*")
        senha_entry.pack()
        tk.Label(self, text="RG").pack()
        rg_entry = tk.Entry(self)
        rg_entry.pack()
        tk.Label(self, text="CPF").pack()
        cpf_entry = tk.Entry(self)
        cpf_entry.pack()
        tk.Label(self, text="Telefone").pack()
        telefone_entry = tk.Entry(self)
        telefone_entry.pack()
        tk.Label(self, text="Endereço").pack()
        endereco_entry = tk.Entry(self)
        endereco_entry.pack()

        def cadastrar_cliente():
            nome = nome_entry.get()
            apelido = apelido_entry.get()
            senha = senha_entry.get()
            rg = rg_entry.get()
            cpf = cpf_entry.get()
            telefone = telefone_entry.get()
            endereco = endereco_entry.get()
            if not nome or not apelido or not senha or not rg or not cpf or not telefone or not endereco:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            cliente = Cliente(nome, rg, cpf, telefone, apelido, senha, endereco)
            cliente.salvar_bd()

        tk.Button(self, text="Cadastrar", command=cadastrar_cliente).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.create_widgets).pack(pady=5)

    def tela_buscar_produto(self):
        self.clear_widgets()
        tk.Label(self, text="Buscar Produto").pack(pady=10)
        tk.Label(self, text="Nome do Produto").pack()
        nome_entry = tk.Entry(self)
        nome_entry.pack()

        def buscar_produto():
            nome = nome_entry.get()
            if not nome:
                messagebox.showerror("Erro", "Digite o nome do produto!")
                return
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM produtos WHERE nome = %s", (nome,))
                produto = cursor.fetchone()
                cursor.close()
                conn.close()
                if produto:
                    produto_obj = Produto(produto[0], produto[1], produto[2], produto[3], produto[4], produto[5], produto[6], produto[7])
                    detalhes = produto_obj.exibir_detalhes()
                    messagebox.showinfo("Detalhes do Produto", detalhes)
                else:
                    messagebox.showwarning("Produto Não Encontrado", "Produto não encontrado no banco de dados.")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

        tk.Button(self, text="Buscar", command=buscar_produto).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.create_widgets).pack(pady=5)

    def tela_listar_produtos(self):
        self.clear_widgets()
        tk.Label(self, text="Listagem de Produtos").pack(pady=10)
        try:
            produtos = Produto.listar_produtos()
            if produtos:
                for produto in produtos:
                    produto_obj = Produto(produto[0], produto[1], produto[2], produto[3], produto[4], produto[5], produto[6], produto[7])
                    detalhes = produto_obj.exibir_detalhes()
                    tk.Label(self, text=detalhes).pack(pady=2)
            else:
                tk.Label(self, text="Nenhum produto encontrado.").pack(pady=2)
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")
        tk.Button(self, text="Voltar", command=self.create_widgets).pack(pady=5)

    def tela_principal_cliente(self):
        self.clear_widgets()
        tk.Label(self, text=f"Bem-vindo(a), {self.usuario_logado.nome}!").pack(pady=10)
        tk.Button(self, text="Buscar Produto", command=self.tela_buscar_produto).pack(pady=5)
        tk.Button(self, text="Listar Produtos", command=self.tela_listar_produtos).pack(pady=5)
        tk.Button(self, text="Novo Pedido", command=self.tela_novo_pedido).pack(pady=5)
        tk.Button(self, text="Sair", command=self.logout).pack(pady=5)

    def tela_principal_funcionario(self):
        self.clear_widgets()
        tk.Label(self, text=f"Bem-vindo(a), {self.usuario_logado.nome}!").pack(pady=10)
        tk.Button(self, text="Cadastrar Produto", command=self.tela_cadastro_produto).pack(pady=5)
        tk.Button(self, text="Buscar Produto", command=self.tela_buscar_produto).pack(pady=5)
        tk.Button(self, text="Listar Produtos", command=self.tela_listar_produtos).pack(pady=5)
        tk.Button(self, text="Excluir Produto", command=self.tela_excluir_produto).pack(pady=5)
        tk.Button(self, text="Sair", command=self.logout).pack(pady=5)

    def tela_cadastro_produto(self):
        self.clear_widgets()
        tk.Label(self, text="Cadastro de Produto").pack(pady=10)
        tk.Label(self, text="ID do Produto").pack()
        id_produto_entry = tk.Entry(self)
        id_produto_entry.pack()
        tk.Label(self, text="Nome").pack()
        nome_entry = tk.Entry(self)
        nome_entry.pack()
        tk.Label(self, text="Preço").pack()
        preco_entry = tk.Entry(self)
        preco_entry.pack()
        tk.Label(self, text="Descrição").pack()
        descricao_entry = tk.Entry(self)
        descricao_entry.pack()
        tk.Label(self, text="Tipo").pack()
        tipo_entry = tk.Entry(self)
        tipo_entry.pack()
        tk.Label(self, text="Marca").pack()
        marca_entry = tk.Entry(self)
        marca_entry.pack()
        tk.Label(self, text="Categoria").pack()
        categoria_entry = tk.Entry(self)
        categoria_entry.pack()
        tk.Label(self, text="Quantidade").pack()
        quantidade_entry = tk.Entry(self)
        quantidade_entry.pack()

        def cadastrar_produto():
            id_produto = id_produto_entry.get()
            nome = nome_entry.get()
            preco = preco_entry.get()
            descricao = descricao_entry.get()
            tipo = tipo_entry.get()
            marca = marca_entry.get()
            categoria = categoria_entry.get()
            quantidade = quantidade_entry.get()
            if not id_produto or not nome or not preco or not descricao or not tipo or not marca or not categoria or not quantidade:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            try:
                preco = float(preco)
                quantidade = int(quantidade)
                produto = Produto(id_produto, nome, preco, descricao, tipo, marca, categoria, quantidade)
                produto.salvar_bd()
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Preço deve ser um número válido e quantidade deve ser um número inteiro.")

        tk.Button(self, text="Cadastrar", command=cadastrar_produto).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.tela_principal_funcionario).pack(pady=5)

    def tela_excluir_produto(self):
        self.clear_widgets()
        tk.Label(self, text="Excluir Produto").pack(pady=10)
        tk.Label(self, text="ID do Produto").pack()
        id_produto_entry = tk.Entry(self)
        id_produto_entry.pack()

        def excluir_produto():
            id_produto = id_produto_entry.get()
            if not id_produto:
                messagebox.showerror("Erro", "Digite o ID do produto!")
                return
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (id_produto,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                else:
                    messagebox.showwarning("Produto Não Encontrado", "Produto não encontrado no banco de dados.")
                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

        tk.Button(self, text="Excluir", command=excluir_produto).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.tela_principal_funcionario).pack(pady=5)

    def tela_novo_pedido(self):
        self.clear_widgets()
        tk.Label(self, text="Novo Pedido").pack(pady=10)
        tk.Label(self, text="ID do Produto").pack()
        id_produto_entry = tk.Entry(self)
        id_produto_entry.pack()
        tk.Label(self, text="Quantidade").pack()
        quantidade_entry = tk.Entry(self)
        quantidade_entry.pack()

        def adicionar_pedido():
            id_produto = id_produto_entry.get()
            quantidade = quantidade_entry.get()
            if not id_produto or not quantidade:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            try:
                quantidade = int(quantidade)
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM produtos WHERE id_produto = %s", (id_produto,))
                produto = cursor.fetchone()
                if produto and produto[6] >= quantidade:
                    pedido = Pedido(id_produto, quantidade, self.usuario_logado.cpf)
                    pedido.salvar_bd()
                    messagebox.showinfo("Sucesso", "Pedido realizado com sucesso!")
                else:
                    messagebox.showwarning("Erro", "Produto não encontrado ou quantidade insuficiente.")
                cursor.close()
                conn.close()
            except ValueError:
                messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

        tk.Button(self, text="Adicionar", command=adicionar_pedido).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.tela_principal_cliente).pack(pady=5)

    def logout(self):
        self.usuario_logado = None
        self.create_widgets()

if __name__ == "__main__":
    app = App()
    app.mainloop()
