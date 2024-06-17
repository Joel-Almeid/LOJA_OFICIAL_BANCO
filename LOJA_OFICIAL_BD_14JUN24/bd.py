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
            for cliente in clientes:
                if cliente.apelido == apelido and cliente.senha == senha:
                    self.usuario_logado = cliente
                    self.tela_principal_cliente()
                    return
            for funcionario in funcionarios:
                if funcionario.apelido == apelido and funcionario.senha == senha:
                    self.usuario_logado = funcionario
                    self.tela_principal_funcionario()
                    return
            messagebox.showerror("Erro", "Apelido ou senha incorretos.")

        tk.Button(self, text="Login", command=realizar_login).pack(pady=10)
        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=10)

    def voltar_menu_inicial(self):
        self.clear_widgets()
        self.create_widgets()

    def tela_cadastro_cliente(self):
        self.clear_widgets()
        tk.Label(self, text="Cadastrar Cliente").pack(pady=10)
        entries = {}
        for field in ["Nome", "RG", "CPF", "Telefone", "Apelido", "Senha", "Endereço"]:
            tk.Label(self, text=field).pack()
            entry = tk.Entry(self)
            entry.pack()
            entries[field] = entry

        def cadastrar_cliente():
            nome = entries["Nome"].get()
            rg = entries["RG"].get()
            cpf = entries["CPF"].get()
            telefone = entries["Telefone"].get()
            apelido = entries["Apelido"].get()
            senha = entries["Senha"].get()
            endereco = entries["Endereço"].get()

            if valida(cpf):
                cliente = Cliente(nome, rg, cpf, telefone, apelido, senha, endereco)
                clientes.append(cliente)
                cliente.salvar_bd()
            else:
                messagebox.showerror("Erro", "CPF inválido.")

        tk.Button(self, text="Cadastrar", command=cadastrar_cliente).pack(pady=10)
        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=10)

    def tela_cadastro_funcionario(self):
        self.clear_widgets()
        tk.Label(self, text="Cadastrar Funcionário").pack(pady=10)
        entries = {}
        for field in ["Nome", "Apelido", "Senha", "Cargo", "RG", "CPF", "Telefone"]:
            tk.Label(self, text=field).pack()
            entry = tk.Entry(self)
            entry.pack()
            entries[field] = entry

        def cadastrar_funcionario():
            nome = entries["Nome"].get()
            apelido = entries["Apelido"].get()
            senha = entries["Senha"].get()
            cargo = entries["Cargo"].get()
            rg = entries["RG"].get()
            cpf = entries["CPF"].get()
            telefone = entries["Telefone"].get()

            if valida(cpf):
                funcionario = Funcionario(nome, apelido, senha, cargo, rg, cpf, telefone)
                funcionarios.append(funcionario)
                funcionario.salvar_bd()
            else:
                messagebox.showerror("Erro", "CPF inválido.")

        tk.Button(self, text="Cadastrar", command=cadastrar_funcionario).pack(pady=10)
        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=10)

    def tela_principal_cliente(self):
        self.clear_widgets()
        tk.Label(self, text=f"Bem-vindo, {self.usuario_logado.nome}!").pack(pady=10)
        tk.Button(self, text="Buscar Produto", command=self.tela_buscar_produto).pack(pady=5)
        tk.Button(self, text="Listar Produtos", command=self.tela_listar_produtos).pack(pady=5)
        tk.Button(self, text="Adicionar Produto ao Pedido", command=self.tela_adicionar_produto_pedido).pack(pady=5)
        tk.Button(self, text="Ver Endereço", command=self.ver_endereco).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=10)

    def tela_principal_funcionario(self):
        self.clear_widgets()
        tk.Label(self, text=f"Bem-vindo, {self.usuario_logado.nome}!").pack(pady=10)
        tk.Button(self, text="Cadastrar Produto", command=self.tela_cadastrar_produto).pack(pady=5)
        tk.Button(self, text="Listar Produtos", command=self.tela_listar_produtos).pack(pady=5)
        tk.Button(self, text="Excluir Produto", command=self.tela_excluir_produto).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=10)

    def tela_buscar_produto(self):
        self.clear_widgets()
        tk.Label(self, text="Buscar Produto").pack(pady=10)
        tk.Label(self, text="Nome do Produto").pack()
        nome_entry = tk.Entry(self)
        nome_entry.pack()

        def buscar():
            nome = nome_entry.get()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM produtos WHERE nome LIKE %s", (f"%{nome}%",))
                produtos = cursor.fetchall()
                cursor.close()
                conn.close()
                if produtos:
                    result_text = "\n".join(
                        [f"Nome: {produto[1]}, Preço: {produto[2]}, Quantidade: {produto[7]}" for produto in produtos])
                    messagebox.showinfo("Produtos Encontrados", result_text)
                else:
                    messagebox.showinfo("Sem Resultados", "Nenhum produto encontrado.")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

        tk.Button(self, text="Buscar", command=buscar).pack(pady=10)
        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=10)

    def tela_listar_produtos(self):
        self.clear_widgets()
        tk.Label(self, text="Lista de Produtos").pack(pady=10)

        produtos = Produto.listar_produtos()
        for produto in produtos:
            tk.Label(self, text=f"ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}, Quantidade: {produto[7]}").pack()

        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=10)

    def tela_adicionar_produto_pedido(self):
        self.clear_widgets()
        tk.Label(self, text="Adicionar Produto ao Pedido").pack(pady=10)
        tk.Label(self, text="ID do Produto").pack()
        id_produto_entry = tk.Entry(self)
        id_produto_entry.pack()
        tk.Label(self, text="Quantidade").pack()
        quantidade_entry = tk.Entry(self)
        quantidade_entry.pack()

        def adicionar():
            id_produto = int(id_produto_entry.get())
            quantidade = int(quantidade_entry.get())
            produto = None
            for prod in produtos:
                if prod.id_produto == id_produto:
                    produto = prod
                    break
            if produto:
                self.pedido_atual.adicionar_produto(produto, quantidade)
            else:
                messagebox.showerror("Erro", "Produto não encontrado.")

        tk.Button(self, text="Adicionar", command=adicionar).pack(pady=10)
        tk.Button(self, text="Voltar", command=self.tela_principal_cliente).pack(pady=10)

    def realizar_pagamento(self):
        self.clear_widgets()
        tk.Label(self, text="Realizar Pagamento").pack(pady=10)
        tk.Label(self, text="Forma de Pagamento").pack()
        forma_pagamento_entry = tk.Entry(self)
        forma_pagamento_entry.pack()

        def pagar():
            forma_pagamento = forma_pagamento_entry.get()
            self.pedido_atual.selecionar_forma_pagamento(forma_pagamento)
            self.pedido_atual.realizar_pagamento()

        tk.Button(self, text="Pagar", command=pagar).pack(pady=10)
        tk.Button(self, text="Voltar", command=self.tela_principal_cliente).pack(pady=10)

    def tela_cadastrar_produto(self):
        self.clear_widgets()
        tk.Label(self, text="Cadastrar Produto").pack(pady=10)
        entries = {}
        for field in ["ID do Produto", "Nome", "Preço", "Descrição", "Tipo", "Marca", "Categoria", "Quantidade"]:
            tk.Label(self, text=field).pack()
            entry = tk.Entry(self)
            entry.pack()
            entries[field] = entry

        def cadastrar_produto():
            id_produto = int(entries["ID do Produto"].get())
            nome = entries["Nome"].get()
            preco = float(entries["Preço"].get())
            descricao = entries["Descrição"].get()
            tipo = entries["Tipo"].get()
            marca = entries["Marca"].get()
            categoria = entries["Categoria"].get()
            quantidade = int(entries["Quantidade"].get())

            produto = Produto(id_produto, nome, preco, descricao, tipo, marca, categoria, quantidade)
            produtos.append(produto)
            produto.salvar_bd()

        tk.Button(self, text="Cadastrar", command=cadastrar_produto).pack(pady=10)
        tk.Button(self, text="Voltar", command=self.tela_principal_funcionario).pack(pady=10)

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



if __name__== "__main__":
    app = App()
    app.mainloop()