class Endereco:
    def __init__(self, rua, numero, complemento, bairro, cidade, uf):
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf

class Cliente:
    def __init__(self, cpf, nome, data_nascimento, endereco, qtd_saques=0):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []
        self.qtd_saques = qtd_saques

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Conta:
    def __init__(self, cliente, numero_conta, agencia, extrato=None):
        self.cliente = cliente
        self.numero_conta = numero_conta
        self.agencia = agencia
        if extrato is None:
            self.extrato = []
        else:
            self.extrato = extrato

    @property
    def saldo(self):
        return sum(self.extrato)

    def depositar(self, valor):
        if valor > 0:
            self.extrato.append(valor)
            return True
        else:
            print('Valor não pode ser negativo')
            return False

    def retirar(self, valor):
        if self.cliente.qtd_saques > LIMITE_SAQUES:
            print(f'Valor excede limite de saque. Limite: R$ {self.cliente.qtd_saques}')
            return False
        elif valor > self.saldo:
            print('Saldo insuficiente para saque.')
            return False
        else:
            self.extrato.append(-valor)
            return True

    def listar_extrato(self):
        if not self.extrato:
            print('Não foram realizadas movimentações!')
        else:
            print("==========================================")
            print(f"CPF: {self.cliente.cpf}")
            print(f"Agência: {self.agencia}")
            print(f"C/C: {self.numero_conta}")
            print(f"Titular: {self.cliente.nome}")
            print("==========================================")
            print("Início Extrato")
            for item in self.extrato:
                if item >= 0:
                    print(f'\tC R$ {item}')
                else:
                    print(f'\tD R$ {item}')
            print(f"\n\tSaldo: R$ {self.saldo}")
            print("Fim Extrato")
            print("==========================================")

AGENCIA = "0001"
LIMITE_DIARIO = 500
LIMITE_SAQUES = 3

clientes = []

def retira_sinais(texto):
    resultado = ''
    for caractere in texto:
        if caractere.isdigit():
            resultado += caractere
    return resultado

def menu_conta():
    tela = """
            Movimentação de Conta Corrente

                Selecione uma opção:
                [C]adastrar Cliente
                [I]ncluir Conta
                [P]osicionar Cliente/Conta
                [L]istar Contas

                [S]air
        => """
    return input(tela)

def menu_opcoes():
    tela = """
            Movimentação de Conta Corrente

                Selecione uma opção:
                [D]epositar
                [R]etirar
                [E]xtrato

                [V]oltar
        => """
    return input(tela)

def saldo_conta(conta):
    return sum(conta.extrato)

def selecionar_cliente(cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def selecionar_conta(cpf, numero_conta):
    cliente = selecionar_cliente(cpf)
    if cliente:
        for conta in cliente.contas:
            if conta.numero_conta == numero_conta:
                return conta
    return None

def listar_contas():
    print("==========================================")
    print("Início da Listagem")
    for cliente in clientes:
        for conta in cliente.contas:
            saldo = conta.saldo
            print(f"""
                Agência: {conta.agencia}
                C/C: {conta.numero_conta}
                Titular: {cliente.nome}
                Saldo: {saldo}
            """)
    print("Fim da Listagem")
    print("==========================================")

def criar_conta(cliente):
    if cliente:
        numero_conta = len(cliente.contas) + 1
        conta = Conta(cliente, numero_conta, AGENCIA)
        cliente.adicionar_conta(conta)
        return conta
    else:
        print("Cliente não cadastrado!")

def solicitar_numero_conta():
    while True:
        numero_conta = input("Número da conta: ")
        if numero_conta.isdigit():
            return int(numero_conta)
        else:
            print("Por favor, insira apenas números inteiros para o número da conta.")

def depositar(conta):
    valor = float(input("Entre com o valor do depósito: "))
    if valor > 0:
        conta.depositar(valor)
    else:
        print('Valor não pode ser negativo')

def retirar(numero_saques, conta):
    if numero_saques < LIMITE_SAQUES:
        valor = float(input("Entre com o valor de saque: "))
        if valor < 0:
            print('Valor não pode ser negativo')
        else:
            conta.retirar(valor)
            return numero_saques + 1
    else:
        print('Limite de saques diários atingido (Máximo 3)')
    return numero_saques

def lista_extrato(cpf, conta):
    conta.listar_extrato()

while True:
    opcao = menu_conta().upper()

    if opcao == 'C':
        cpf = input("CPF: ")
        nome = input("Nome: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        rua = input("Rua: ")
        numero = input("Número: ")
        complemento = input("Complemento: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        uf = input("UF: ")
        endereco = Endereco(rua, numero, complemento, bairro, cidade, uf)
        clientes.append(Cliente(cpf, nome, data_nascimento, endereco))
        print("Cliente cadastrado com sucesso!")

    elif opcao == 'I':
        cpf = input("CPF do cliente: ")
        cliente = selecionar_cliente(cpf)
        conta = criar_conta(cliente)
        if conta:
            print("Conta cadastrada com sucesso!")

    elif opcao == 'L':
        listar_contas()

    elif opcao == 'P':
        cpf = input("CPF do cliente: ")
        numero_conta = solicitar_numero_conta()
        conta = selecionar_conta(cpf, numero_conta)
        
        opcao_conta = ''
        numero_saques = 0
        while opcao_conta != 'V':
            opcao_conta = menu_opcoes().upper()
            if opcao_conta == 'D':
                depositar(conta)
            elif opcao_conta == 'R':
                numero_saques = retirar(numero_saques, conta)
            elif opcao_conta == 'E':                
                lista_extrato(cpf, conta)
            elif opcao_conta == 'V':
                break
            else:
                print("Opção inválida!")

    elif opcao == 'S':
        break

    else:
        print("Opção inválida!")
