import tkinter as tk
from tkinter import messagebox


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


class Funcionario(Usuario):
    def __init__(self, nome, apelido, senha, cargo, rg, cpf, telefone):
        super().__init__(nome, apelido, senha, rg, cpf, telefone)
        self.cargo = cargo


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

    def create_widgets(self):
        tk.Label(self, text="Bem-vindo à WEB TECHNOMUSIC!").pack(pady=10)
        tk.Button(self, text="Login", command=self.tela_login).pack(pady=5)
        tk.Button(self, text="Cadastrar Funcionário", command=self.tela_cadastro_funcionario).pack(pady=5)
        tk.Button(self, text="Cadastrar Cliente", command=self.tela_cadastro_cliente).pack(pady=5)
        tk.Button(self, text="Buscar Produto", command=self.tela_buscar_produto).pack(pady=5)
        tk.Button(self, text="Sair", command=self.quit).pack(pady=5)

    def tela_login(self):
        self.clear_widgets()
        tk.Label(self, text="Login").pack(pady=10)
        tk.Label(self, text="Apelido").pack()
        apelido_entry = tk.Entry(self)
        apelido_entry.pack()
        tk.Label(self, text="Senha").pack()
        senha_entry = tk.Entry(self, show='*')
        senha_entry.pack()
        tk.Button(self, text="Login", command=lambda: self.fazer_login(apelido_entry.get(), senha_entry.get())).pack(
            pady=5)
        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=5)

    def fazer_login(self, apelido, senha):
        for usuario in clientes + funcionarios:
            if usuario.apelido == apelido and usuario.senha == senha:
                self.usuario_logado = usuario
                messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario.nome}!")
                self.show_menu_usuario()
                return
        messagebox.showwarning("Erro", "Usuário ou senha inválidos. Por favor, tente novamente.")

    def tela_cadastro_funcionario(self):
        self.clear_widgets()
        tk.Label(self, text="Cadastro de Funcionário").pack(pady=10)
        campos = ["Nome", "gmail", "Cargo", "Senha", "Data de Nascimento", "CPF", "Telefone"]
        entradas = {campo: tk.Entry(self) for campo in campos}
        for campo, entrada in entradas.items():
            tk.Label(self, text=campo).pack()
            entrada.pack()
        tk.Button(self, text="Cadastrar", command=lambda: self.cadastrar_funcionario(entradas)).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=5)

    def cadastrar_funcionario(self, entradas):
        dados = {campo: entrada.get() for campo, entrada in entradas.items()}
        if valida(dados["CPF"]):
            func = Funcionario(dados["Nome"], dados["gmail"], dados["Senha"], dados["Cargo"],
                               dados["Data de Nascimento"], dados["CPF"], dados["Telefone"])
            funcionarios.append(func)
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso")
        else:
            messagebox.showwarning("Erro", "CPF inválido.")

    def tela_cadastro_cliente(self):
        self.clear_widgets()
        tk.Label(self, text="Cadastro de Cliente").pack(pady=10)
        campos = ["Nome", "Data de Nascimento", "CPF", "Telefone", "Email:", "Senha", "Endereço"]
        entradas = {campo: tk.Entry(self) for campo in campos}
        for campo, entrada in entradas.items():
            tk.Label(self, text=campo).pack()
            entrada.pack()
        tk.Button(self, text="Cadastrar", command=lambda: self.cadastrar_cliente(entradas)).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=5)

    def cadastrar_cliente(self, entradas):
        dados = {campo: entrada.get() for campo, entrada in entradas.items()}
        if valida(dados["CPF"]):
            cli = Cliente(dados["Nome"], dados["Data de Nascimento"], dados["CPF"], dados["Telefone"], dados["Email:"],
                          dados["Senha"], dados["Endereço"])
            clientes.append(cli)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso")
        else:
            messagebox.showwarning("Erro", "CPF inválido.")

    def tela_buscar_produto(self):
        self.clear_widgets()
        tk.Label(self, text="Buscar Produto").pack(pady=10)
        tk.Label(self, text="Nome do Produto").pack()
        nome_entry = tk.Entry(self)
        nome_entry.pack()
        tk.Button(self, text="Buscar", command=lambda: self.buscar_produto_e_ver_descricao(nome_entry.get())).pack(
            pady=5)
        tk.Button(self, text="Voltar", command=self.voltar_menu_inicial).pack(pady=5)

    def buscar_produto_e_ver_descricao(self, nome):
        for produto in produtos:
            if produto.nome == nome:
                messagebox.showinfo("Produto Encontrado", produto.exibir_detalhes())
                return
        messagebox.showwarning("Erro", "Produto não encontrado.")

    def show_menu_usuario(self):
        self.clear_widgets()
        if isinstance(self.usuario_logado, Cliente):
            self.menu_cliente()
        elif isinstance(self.usuario_logado, Funcionario):
            self.menu_funcionario()

    def menu_cliente(self):
        tk.Label(self, text=f"Bem-vindo, {self.usuario_logado.nome}!").pack(pady=10)
        tk.Button(self, text="Realizar Pedido", command=self.realizar_pedido_cliente).pack(pady=5)
        tk.Button(self, text="Alterar Endereço", command=self.alterar_endereco_cliente).pack(pady=5)
        tk.Button(self, text="Ver Endereço", command=self.ver_endereco_cliente).pack(pady=5)
        tk.Button(self, text="Adicionar Produto no Carrinho", command=self.adicionar_produto_carrinho).pack(pady=5)
        tk.Button(self, text="Buscar Produto", command=self.tela_buscar_produto).pack(pady=5)
        tk.Button(self, text="Sair", command=self.voltar_menu_inicial).pack(pady=5)

    def menu_funcionario(self):
        tk.Label(self, text=f"Bem-vindo, {self.usuario_logado.nome}!").pack(pady=10)
        tk.Button(self, text="Cadastrar Produto", command=self.tela_cadastro_produto).pack(pady=5)
        tk.Button(self, text="Ver Produtos Cadastrados", command=self.ver_produtos_cadastrados).pack(pady=5)
        tk.Button(self, text="Excluir Produto", command=self.tela_excluir_produto).pack(pady=5)
        tk.Button(self, text="Realizar Entrega", command=self.realizar_entrega).pack(pady=5)
        tk.Button(self, text="Buscar Cliente", command=self.buscar_cliente).pack(pady=5)
        tk.Button(self, text="Buscar Funcionário", command=self.buscar_funcionario).pack(pady=5)
        tk.Button(self, text="Sair", command=self.voltar_menu_inicial).pack(pady=5)

    def adicionar_produto_carrinho(self):
        self.clear_widgets()
        tk.Label(self, text="Adicionar Produto no Carrinho").pack(pady=10)
        tk.Label(self, text="Nome do Produto").pack()
        nome_entry = tk.Entry(self)
        nome_entry.pack()
        tk.Label(self, text="Quantidade").pack()
        quantidade_entry = tk.Entry(self)
        quantidade_entry.pack()
        tk.Button(self, text="Adicionar",
                  command=lambda: self.adicionar_ao_pedido(nome_entry.get(), int(quantidade_entry.get()))).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.menu_cliente).pack(pady=5)

    def realizar_pedido_cliente(self):
        self.clear_widgets()
        tk.Label(self, text="Realizar Pedido").pack(pady=10)
        tk.Label(self, text="Forma de Pagamento (dinheiro/cartao)").pack()
        pagamento_entry = tk.Entry(self)
        pagamento_entry.pack()
        tk.Button(self, text="Finalizar Pedido", command=lambda: self.finalizar_pedido(pagamento_entry.get())).pack(
            pady=5)
        tk.Button(self, text="Voltar", command=self.menu_cliente).pack(pady=5)

    def adicionar_ao_pedido(self, nome, quantidade):
        if self.pedido_atual is None:
            self.pedido_atual = Pedido()
        for produto in produtos:
            if produto.nome == nome:
                self.pedido_atual.adicionar_produto(produto, quantidade)
                return
        messagebox.showwarning("Erro", "Produto não encontrado.")

    def finalizar_pedido(self, forma_pagamento):
        if self.pedido_atual:
            self.pedido_atual.selecionar_forma_pagamento(forma_pagamento)
            self.pedido_atual.realizar_pagamento()
            self.pedido_atual = None
        else:
            messagebox.showwarning("Erro", "Nenhum pedido em andamento.")

    def alterar_endereco_cliente(self):
        self.clear_widgets()
        tk.Label(self, text="Alterar Endereço").pack(pady=10)
        tk.Label(self, text="Novo Endereço").pack()
        endereco_entry = tk.Entry(self)
        endereco_entry.pack()
        tk.Button(self, text="Alterar",
                  command=lambda: self.usuario_logado.alterar_endereco(endereco_entry.get())).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.menu_cliente).pack(pady=5)

    def ver_endereco_cliente(self):
        self.clear_widgets()
        tk.Label(self, text="Endereço do Cliente").pack(pady=10)
        tk.Label(self, text=self.usuario_logado.endereco).pack(pady=10)
        tk.Button(self, text="Voltar", command=self.menu_cliente).pack(pady=5)

    def tela_cadastro_produto(self):
        self.clear_widgets()
        tk.Label(self, text="Cadastro de Produto").pack(pady=10)
        campos = ["ID do Produto", "Nome", "Preço", "Descrição", "Tipo", "Marca", "Categoria", "Quantidade"]
        entradas = {campo: tk.Entry(self) for campo in campos}
        for campo, entrada in entradas.items():
            tk.Label(self, text=campo).pack()
            entrada.pack()
        tk.Button(self, text="Cadastrar", command=lambda: self.cadastrar_produto(entradas)).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.menu_funcionario).pack(pady=5)

    def cadastrar_produto(self, entradas):
        dados = {campo: entrada.get() for campo, entrada in entradas.items()}
        try:
            preco = float(dados["Preço"])
            quantidade = int(dados["Quantidade"])
            prod = Produto(dados["ID do Produto"], dados["Nome"], preco, dados["Descrição"], dados["Tipo"],
                           dados["Marca"], dados["Categoria"], quantidade)
            produtos.append(prod)
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")
        except ValueError:
            messagebox.showwarning("Erro", "Preço ou Quantidade inválidos.")

    def excluir_produto(self, nome):
        for produto in produtos:
            if produto.nome == nome:
                produtos.remove(produto)
                messagebox.showinfo("Sucesso", f"Produto {nome} excluído com sucesso")
                return
        messagebox.showwarning("Erro", "Produto não encontrado")

    def tela_excluir_produto(self):
        self.clear_widgets()
        tk.Label(self, text="Excluir Produto").pack(pady=10)
        tk.Label(self, text="Nome do Produto").pack()
        nome_entry = tk.Entry(self)
        nome_entry.pack()
        tk.Button(self, text="Excluir", command=lambda: self.excluir_produto(nome_entry.get())).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.menu_funcionario).pack(pady=5)



    def realizar_entrega(self):
        messagebox.showinfo("Entrega", "Realizando entrega...")
        # Simulação de tempo para entrega
        self.after(2000, lambda: messagebox.showinfo("Sucesso", "Entrega realizada com sucesso!"))

    def buscar_cliente(self):
        self.clear_widgets()
        tk.Label(self, text="Buscar Cliente").pack(pady=10)
        tk.Label(self, text="Nome do Cliente").pack()
        nome_entry = tk.Entry(self)
        nome_entry.pack()
        tk.Button(self, text="Buscar", command=lambda: self.buscar_cliente_por_nome(nome_entry.get())).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.menu_funcionario).pack(pady=5)

    def buscar_cliente_por_nome(self, nome):
        for cliente in clientes:
            if cliente.nome == nome:
                messagebox.showinfo("Cliente Encontrado",
                                    f"Cliente encontrado: {cliente.nome}\nEmail: {cliente.email}\nEndereço: {cliente.endereco}")
                return
        messagebox.showwarning("Erro", "Cliente não encontrado.")

    def buscar_funcionario(self):
        self.clear_widgets()
        tk.Label(self, text="Buscar Funcionário").pack(pady=10)
        tk.Label(self, text="Nome do Funcionário").pack()
        nome_entry = tk.Entry(self)
        nome_entry.pack()
        tk.Button(self, text="Buscar", command=lambda: self.buscar_funcionario_por_nome(nome_entry.get())).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.menu_funcionario).pack(pady=5)

    def buscar_funcionario_por_nome(self, nome):
        for funcionario in funcionarios:
            if funcionario.nome == nome:
                messagebox.showinfo("Funcionário Encontrado",
                                    f"Funcionário encontrado: {funcionario.nome}\nEmail: {funcionario.email}\nCargo: {funcionario.cargo}")
                return
        messagebox.showwarning("Erro", "Funcionário não encontrado.")

    def ver_produtos_cadastrados(self):
        self.clear_widgets()
        tk.Label(self, text="Produtos Cadastrados").pack(pady=10)
        produtos_lista = "\n".join(
            [f"{produto.nome} - R${produto.preco:.2f} - Quantidade: {produto.quantidade} - ID Produto:" for produto in produtos])
        tk.Label(self, text=produtos_lista).pack(pady=10)
        tk.Button(self, text="Voltar", command=self.menu_funcionario).pack(pady=5)

    def voltar_menu_inicial(self):
        self.usuario_logado = None
        self.pedido_atual = None
        self.clear_widgets()
        self.create_widgets()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()