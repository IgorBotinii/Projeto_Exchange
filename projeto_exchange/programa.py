from datetime import datetime
import random
nome_usuario = ""  # Inicializando o nome do usuário fora do loop

while True:
    print("Seja Bem-Vindo ao FEINANCE, a principal exchange de compra e venda em criptomoeda, digite seu login para continuar")

    # PERGUNTA SE O USUARIO JA POSSUI CADASTRO
    NumSelect =  int(input("Ja possui cadastro? 1 -> SIM // 2 -> NÃO: "))
    if NumSelect == 2:
        nome_usuario = input("Digite seu nome: ")
        cpf_user = input("Digite seu CPF (Somente Numeros): ")
        senha_user = input("Digite a sua senha: ")
        saldo_reais = 0
        saldo_bitcoin = 0
        saldo_ripple = 0
        saldo_ethereum = 0

        
        # CODIGO ABAIXO SERVE PARA INSERIR OS DADOS NO ARQUIVO TXT
        with open('Bd_Usuarios.txt','a') as bd_arquivos:
            bd_arquivos.write(cpf_user + '\n')
            bd_arquivos.write(senha_user + '\n')
            bd_arquivos.write(nome_usuario + '\n')
            bd_arquivos.write("Reais: " + str(saldo_reais) + '\n')
            bd_arquivos.write("Bitcoin: " + str(saldo_bitcoin) + '\n')
            bd_arquivos.write("Ripple: " + str(saldo_ripple) + '\n')
            bd_arquivos.write("Ethereum: " + str(saldo_ethereum) + '\n')
        print("Informações Inseridas com sucesso!")

    # CODIGO ABAIXO SERVE PARA VER AS INFORMAÇÕES DO USUARIO E VER NO DB SE JA POSSUI CADASTRO
    else:
        cpf_user_login = input("Digite seu CPF (Somente Números): ")
        cpf_login_sacar = cpf_user_login
        senha_user_login = input("Digite a sua senha: ")
        login_correto = False

        # LISTA ABAIXO SERVE PARA GUARDAR AS INFORMAÇÕES DO TXT, PRA DPS VERIFICAR DENTRO DELE SE EXISTEM AS INFORMAÇÕES INSERIDAS
        dados = []
                      
        with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
            for linha in bd_arquivos:
                dados.append(linha.strip()) #Strip remove todos os espaços

        # VERIFICA O CPF
        if cpf_user_login in dados:
            # Obtendo o indice do CPF fornecido
            indice_cpf = dados.index(cpf_user_login)
            # Verificando se a senha bate com o CPF
            if senha_user_login == dados[indice_cpf + 1]:
                print(" ")
                print("Login realizado com sucesso!")
                print(" ")
                login_correto = True
                nome_usuario = dados[indice_cpf + 2]  # Atualiza o nome do usuário globalmente
            else:
                print("Senha incorreta, verifique e tente novamente.")
        else:
            print("CPF não encontrado. Verifique se digitou corretamente ou faça um novo cadastro.")

        if not login_correto:
            continue  # Se o login não estiver correto, reinicia o loop

        # Após o login bem-sucedido, obtemos o CPF do usuário
        cpf_user_login = cpf_user_login

        break  # Se o login estiver correto, saia do loop de cadastro/login


# FUNÇÃO DEPOSITO // EXTRATO OK
def Deposito(cpf_user_login):
    valor_deposito = float(input("Digite o valor do deposito: "))
    
    # Abrindo o arquivo e lendo todas as linhas
    with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
        linhas = bd_arquivos.readlines()

    encontrado = False
    # Procurando pelo CPF do usuário no arquivo
    for i in range(0, len(linhas), 7): # Lendo quantas linhas tem em cada cadastro de usuario
        if linhas[i].strip() == cpf_user_login:
            saldo_usuario = float(linhas[i + 3].split(":") [1])  # Obtendo o saldo do usuario
            novo_saldo = saldo_usuario + valor_deposito  # Calculando o novo saldo
            linhas[i + 3] = f"Reais: {novo_saldo}\n"  # Atualizando o saldo no arquivo
            encontrado = True
            break
    if encontrado:
        # Escrevendo as linhas atualizadas no arquivo
        with open('Bd_Usuarios.txt', 'w') as bd_arquivos:
            bd_arquivos.writelines(linhas)
        
        print("Depósito realizado com sucesso. Digite 1 para consultar seu saldo ")
        #INSERINDO EXTRATO NO TXT
        now = datetime.now()
        data_hora = now.strftime("%d-%m-%Y %H:%M")  # FORMATO (DD/MM/AAA HORA)
        
        with open('bd_extrato.txt','a') as bd_extrato:
            bd_extrato.write(f"{data_hora} + {valor_deposito:.2f} REAL CT: 0.0    TX: 0.00 REAL: {novo_saldo:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")
# FUNÇÃO CONSULTA DE SALDO 
def Consultar_saldo(cpf_user_login):
    global nome_usuario  # Declaração de variável global, para que no print, ele apareça o nome:
    senha_user_login = input("Digite a sua senha: ")

    with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
        linhas = bd_arquivos.readlines()

    encontrado = False
    # Procurando pelo CPF do usuário no arquivo
    for i in range(0, len(linhas), 7):  # Avançando de 7 em 7 linhas para ver os dados de cada usuário
        if i + 6 < len(linhas):  # Verifica se o índice está dentro dos limites da lista
            if linhas[i].strip() == cpf_user_login and linhas[i + 1].strip() == senha_user_login:
                saldo_usuario = float(linhas[i + 3].split(":")[1])  # PEGANDO O SALDO DE REAIS
                saldo_bitcoin = float(linhas[i + 4].split(":")[1])  # PEGANDO O SALDO DE BITCOIN
                saldo_ripple = float(linhas[i + 5].split(":")[1])  # PEGANDO O SALDO DE RIPPLE
                saldo_ethereum = float(linhas[i + 6].split(":")[1])  # PEGANDO O SALDO DE ETHEREUM
                encontrado = True
                break  # Encerra o loop assim que encontrar o usuário e a senha estiver correta

    if encontrado:
        print(" ")
        print("Nome:", nome_usuario)
        print("CPF:", cpf_user_login)
        print(" ")
        print("Reais:", saldo_usuario)
        print("Bitcoin: ", saldo_bitcoin)
        print("Ethereum: ", saldo_ethereum)
        print("Ripple: ", saldo_ripple)
        print("                                                ")
    else:
        print("Senha incorreta ou CPF não encontrado.")
# FUNÇÃO DE SACAR FUNDOS DA CARTEIRA // EXTRATO OK
def sacar_fundo(cpf_user_login):

    valor_saque = float(input("Digite o valor do saque: "))

    # Abrindo o arquivo e lendo todas as linhas
    with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
        linhas = bd_arquivos.readlines()

    encontrado = False
    # Procurando pelo CPF do usuário no arquivo
    for i in range(0, len(linhas), 4):  # Avançando de 4 em 4 linhas para lidar com os dados de cada usuário
        if linhas[i].strip() == cpf_user_login:
            saldo_usuario = float(linhas[i + 3].split(":")[1])  # Obtendo o saldo do usuário
            if valor_saque <= saldo_usuario:  # Verificando se o saldo é suficiente
                novo_saldo = saldo_usuario - valor_saque  # Calculando o novo saldo
                linhas[i + 3] = f"Reais: {novo_saldo}\n"  # Atualizando o saldo no arquivo
                encontrado = True
                break 
            else:
                print("Saldo insuficiente.")
                  

    if encontrado:
        # Escrevendo as linhas atualizadas no arquivo
        with open('Bd_Usuarios.txt', 'w') as bd_arquivos:
            bd_arquivos.writelines(linhas)
        print("                                                ")
        print("Saque realizado com sucesso")
        print("                                                ")

        # INSERINDO NO EXTRATO A INFORMAÇÃO DE RETIRADA NO TXT
        now = datetime.now()
        data_hora = now.strftime("%d-%m-%Y %H:%M")  # FORMATO (DD/MM/AAA HORA)
        
        with open('bd_extrato.txt','a') as bd_extrato:
            bd_extrato.write(f"{data_hora} - {valor_saque:.2f} REAL CT: 0.0    TX: 0.00 REAL: {valor_saque:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")

        print("Informações Inseridas com sucesso!")

    else:
        print("                                                ")
        print("Saldo insuficiente.")
        print("                                                ")
# FUNÇÃO DE COMPRAR CRIPTOS
def Comprar_criptos(cpf_user_login):

    menu_cripto = [
        "1 - Bitcoin",
        "2 - Ripple",
        "3 - Ethereum"
    ]
    for item_cripto in menu_cripto:
        print(item_cripto)
        # espaço
        print() 

    VarOpcaoCripto = int(input("Digite a opção desejada: "))  
########## BITCOIN ########### BITCOIN ################### BITCOIN ########### BITCOIN ################################################################################################      

# BITCOIN OK
    if VarOpcaoCripto == 1:
        ValorCompraMoeda = float(input("Digite o valor que gostaria de comprar: "))
        taxa_bit = ValorCompraMoeda * 0.02 # calcula a taxa

        ValCompraTaxaBit = ValorCompraMoeda - taxa_bit

        # Abrindo o arquivo e lendo todas as linhas
        with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
            linhas = bd_arquivos.readlines()

        encontrado = False
        # Procurando pelo CPF do usuário no arquivo
        for i in range(0, len(linhas), 7): # Lendo quantas linhas tem em cada cadastro de usuario
            if linhas[i].strip() == cpf_user_login and i + 6 < len(linhas):
                saldo_usuario = float(linhas[i + 3].split(":")[1])  # Obtendo o saldo do usuário
                if saldo_usuario >= ValorCompraMoeda:
                    novo_saldo = saldo_usuario - ValorCompraMoeda  # Calculando o novo saldo
                    linhas[i + 3] = f"Reais:{novo_saldo:.2f}\n"  # Atualizando o saldo no arquivo
                    
                    with open('cotacoes.txt','r') as bd_cotacoes:
                        cot = bd_cotacoes.readlines()
                    for c in cot:
                        moeda, valor = c.strip().split(':')
                        if moeda.lower() == 'bitcoin':
                            cot_bit = float(valor)
                            print(f"Valor atual do Bitcoin: ${cot_bit:.2f}")  

                    if i + 4 < len(linhas):  # Verifica se o índice está dentro dos limites da lista
                        saldo_bitcoin_bd = float(linhas[i + 4].split(":")[1]) # I + 4 pois o valor do bitcoin est na linha 4
                        saldo_bit_tx = (saldo_bitcoin_bd + ValCompraTaxaBit) / cot_bit  # Calculando o novo saldo
                        linhas[i + 4] = f"Bitcoin:{saldo_bit_tx:.4f}\n"  # Atualizando o saldo no arquivo
    
                    encontrado = True
                    break

        if encontrado:
            # Escrevendo as linhas atualizadas no arquivo
            with open('Bd_Usuarios.txt', 'w') as bd_arquivos:
                bd_arquivos.writelines(linhas)

            print("Compra de Bitcoin realizada com sucesso. Digite 1 para consultar seu saldo.")

            #EXTRATO
           
            now = datetime.now()
            data_hora = now.strftime("%d-%m-%Y %H:%M")  # FORMATO (DD/MM/AAA HORA)
        
            with open('bd_extrato.txt','a') as bd_extrato:
                bd_extrato.write(f"{data_hora} + {saldo_bit_tx:.2f} BTC CT: 0.0   TX: 0.02 REAL: {novo_saldo:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")
                bd_extrato.write(f"{data_hora} - {ValorCompraMoeda:.2f} REAL CT: 0.0   TX: 0.00 REAL: {novo_saldo:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")
        else:
            print("Saldo insuficiente para realizar a compra de Bitcoin.")

########## RIPLE ########### RIPLE ################### RIPLE ########### RIPLE ################################################################################################
# RIPPLE OK

    elif VarOpcaoCripto == 2:
        ValorCompraMoeda = float(input("Digite o valor que gostaria de comprar: "))
        taxa_xrp = ValorCompraMoeda * 0.01
        ValorCompraMoeda_tx = ValorCompraMoeda - taxa_xrp

        # Abrindo o arquivo e lendo todas as linhas
        with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
            linhas = bd_arquivos.readlines()

        encontrado = False
        # Procurando pelo CPF do usuário no arquivo
        for i in range(0, len(linhas), 7): # Lendo quantas linhas tem em cada cadastro de usuario
            if linhas[i].strip() == cpf_user_login and i + 6 < len(linhas):
                saldo_usuario = float(linhas[i + 3].split(":")[1])  # Obtendo o saldo do usuário
                if saldo_usuario >= ValorCompraMoeda:
                    novo_saldo = saldo_usuario - ValorCompraMoeda  # Calculando o novo saldo
                    linhas[i + 3] = f"Reais:{novo_saldo:.2f}\n"  # Atualizando o saldo no arquivo

                    with open('cotacoes.txt','r') as bd_cotacoes:
                        cot = bd_cotacoes.readlines()
                    for c in cot:
                        moeda, valor = c.strip().split(':')
                        if moeda.lower() == 'ripple':
                            cot_xrp = float(valor)
                            print(f"Valor atual do Ripple: ${cot_xrp:.2f}")  

                    if i + 5 < len(linhas):
                        saldo_xrp_bd = float(linhas[i + 5].split(":")[1])
                        val_tot_xrp = (saldo_xrp_bd + ValorCompraMoeda_tx) / cot_xrp
                        linhas[i + 5] = f"Ripple:{val_tot_xrp}\n"  # VERIFICANDO SALDO DE RIPPLE NA MINHA CARTEIRA
                    if i + 5 < len(linhas):  # Verifica se o índice está dentro dos limites da lista
                        saldo_xrp_bd = float(linhas[i + 5].split(":")[1])
                        saldo_riple_tx = saldo_xrp_bd + ValorCompraMoeda_tx  
                        val_tot_xrp = float(saldo_riple_tx / cot_xrp)
                        linhas[i + 5] = f"Ripple:{val_tot_xrp:.4f}\n"
    
                    encontrado = True
                    break

        if encontrado:
            # Escrevendo as linhas atualizadas no arquivo
            with open('Bd_Usuarios.txt', 'w') as bd_arquivos:
                bd_arquivos.writelines(linhas)

            print("Compra de Ripple realizada com sucesso. Digite 1 para consultar seu saldo.")

            #EXTRATO
           
            now = datetime.now()
            data_hora = now.strftime("%d-%m-%Y %H:%M")  # FORMATO (DD/MM/AAA HORA)
        
            with open('bd_extrato.txt','a') as bd_extrato:
                bd_extrato.write(f"{data_hora} + {val_tot_xrp:.2f} XRP CT: 0.0   TX: 0.00 REAL: {novo_saldo:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")
                bd_extrato.write(f"{data_hora} - {ValorCompraMoeda:.2f} REAL CT: 0.0   TX: 0.00 REAL: {novo_saldo:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")



        else:
            print("Saldo insuficiente para realizar a compra de Ripple.")

########## Ethereum ########### Ethereum ################### Ethereum ########### Ethereum ################################################################################################
#
    elif VarOpcaoCripto == 3:
        ValorCompraMoeda = float(input("Digite o valor que gostaria de comprar: "))
        taxa_eth = ValorCompraMoeda * 0.01
        ValorCompraMoedatx_eth = ValorCompraMoeda - taxa_eth

        # Abrindo o arquivo e lendo todas as linhas
        with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
            linhas = bd_arquivos.readlines()

        encontrado = False
        # Procurando pelo CPF do usuário no arquivo
        for i in range(0, len(linhas), 7): # Lendo quantas linhas tem em cada cadastro de usuario
            if linhas[i].strip() == cpf_user_login and i + 6 < len(linhas):
                saldo_usuario = float(linhas[i + 3].split(":")[1])  # Obtendo o saldo do usuário
                if saldo_usuario >= ValorCompraMoeda:
                    novo_saldo = saldo_usuario - ValorCompraMoeda  # Calculando o novo saldo
                    linhas[i + 3] = f"Reais:{novo_saldo:.2f}\n"  # Atualizando o saldo no arquivo
                    
                    with open('cotacoes.txt','r') as bd_cotacoes:
                        cot = bd_cotacoes.readlines()
                    for c in cot:
                        moeda, valor = c.strip().split(':')
                        if moeda.lower() == 'ethereum':
                            cot_eth = float(valor)
                            print(f"Valor atual do Ethereum: ${cot_eth:.2f}")  

                    if i + 6 < len(linhas):
                        saldo_eth_bd = float(linhas[i + 6].split(":")[1])
                        val_tot_eth = (saldo_eth_bd + ValorCompraMoedatx_eth) / cot_eth
                        linhas[i + 6] = f"Ethereum:{val_tot_eth:.4f}\n"  # Atualizando o saldo no arquivo
                    encontrado = True
                    break

        if encontrado:
            # Escrevendo as linhas atualizadas no arquivo
            with open('Bd_Usuarios.txt', 'w') as bd_arquivos:
                bd_arquivos.writelines(linhas)

            print("Compra de Ethereum realizada com sucesso. Digite 1 para consultar seu saldo.")
            #EXTRATO
        
            now = datetime.now()
            data_hora = now.strftime("%d-%m-%Y %H:%M")  # FORMATO (DD/MM/AAA HORA)
        
            with open('bd_extrato.txt','a') as bd_extrato:
                bd_extrato.write(f"{data_hora} + {val_tot_eth:.4f} ETH CT: 0.0   TX: 0.01 REAL: {novo_saldo:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")
                bd_extrato.write(f"{data_hora} - {ValorCompraMoeda:.2f} REAL CT: 0.0   TX: 0.01 REAL: {novo_saldo:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")
        else:
            print("Saldo insuficiente para realizar a compra de Ethereum.")

        
    else:
        print("Digite uma Opção valida")   
# FUNÇÃO DE VENDER CRIPTOS
def vender_cripto(cpf_user_login):

    menu_cripto = [
        "1 - Bitcoin",
        "2 - Ripple",
        "3 - Ethereum"
    ]
    for item_cripto in menu_cripto:
        print(item_cripto)
        print() 

    opcao_cripto = int(input("Digite a opção da moeda que deseja vender: "))
    valor_venda_moeda = float(input("Digite o valor de venda: "))

    # Abrindo o arquivo e lendo todas as linhas
    with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
        linhas = bd_arquivos.readlines()

    encontrado = False

    
    for i in range(0, len(linhas), 7):  # Lendo quantas linhas tem em cada cadastro de usuário
        if linhas[i].strip() == cpf_user_login and i + 6 < len(linhas):
            saldo_usuario = float(linhas[i + 3].split(":")[1])  # Obtendo o saldo do usuário

########## BITCOIN ########### BITCOIN ################### BITCOIN ########### BITCOIN ######## BITCOIN ######## BITCOIN ######## BITCOIN ######## BITCOIN ######## BITCOIN ######## BITCOIN ######## BITCOIN ######## BITCOIN ######## BITCOIN ######## BITCOIN ######## BITCOIN ######## 
#
            if opcao_cripto == 1:
                # Abrindo o arquivo e lendo todas as linhas
                with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
                    linhas = bd_arquivos.readlines()

                encontrado = False
                # Procurando pelo CPF do usuário no arquivo
                for i in range(0, len(linhas), 7):  # Lendo quantas linhas tem em cada cadastro de usuário
                    if linhas[i].strip() == cpf_user_login and i + 6 < len(linhas):
                        saldo_bitcoin_bd = float(linhas[i + 4].split(":")[1])  # Saldo de Bitcoin do usuário

                        # Obtendo a cotação atual do Bitcoin
                        with open('cotacoes.txt', 'r') as bd_cotacoes:
                            cot = bd_cotacoes.readlines()
                        for c in cot:
                            moeda, valor = c.strip().split(':')
                            if moeda.lower() == 'bitcoin':
                                cot_bitcoin = float(valor)

                        # Calculando o valor total dos bitcoins do usuário
                        valor_total_bitcoin = saldo_bitcoin_bd * cot_bitcoin

                        # Calculando o valor da venda em reais
                        valor_venda_reais = valor_venda_moeda * cot_bitcoin

                        # Calculando o valor da taxa de venda
                        taxa_venda = valor_venda_reais * 0.03

                        if saldo_bitcoin_bd >= valor_venda_moeda:
                            novo_saldo_usuario = float(linhas[i + 3].split(":")[1]) + valor_venda_reais - taxa_venda

                            # Calculando o novo saldo de Bitcoin após a venda
                            novo_saldo_bitcoin = saldo_bitcoin_bd - valor_venda_moeda

                            # Atualizando o saldo em reais no arquivo
                            linhas[i + 3] = f"Reais:{novo_saldo_usuario:.2f}\n"

                            # Atualizando o saldo de Bitcoin no arquivo
                            linhas[i + 4] = f"Bitcoin:{novo_saldo_bitcoin:.8f}\n"

                            # Marcando como encontrado
                            encontrado = True

                            # Registrando a venda no extrato
                            now = datetime.now()
                            data_hora = now.strftime("%d-%m-%Y %H:%M")  # FORMATO (DD/MM/AAA HORA)

                            with open('bd_extrato.txt', 'a') as bd_extrato:
                                bd_extrato.write(f"{data_hora} - {valor_venda_moeda:.8f} BTC CT: 0.0   TX: {taxa_venda:.2f} REAL: {novo_saldo_usuario:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")
                                bd_extrato.write(f"{data_hora} + {valor_venda_reais:.2f} REAL CT: 0.0   TX: 0.00 REAL: {novo_saldo_usuario:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")

                            # Saindo do loop
                            break

                if encontrado:
                    # Escrevendo as linhas atualizadas no arquivo
                    with open('Bd_Usuarios.txt', 'w') as bd_arquivos:
                        bd_arquivos.writelines(linhas)

                    print("Venda de Bitcoin realizada com sucesso. Digite 1 para consultar seu saldo.")
                else:
                    print("Saldo insuficiente para realizar a venda de Bitcoin.")




########## RIPPLE ########### RIPPLE ################### RIPPLE ########### RIPPLE ########
            if opcao_cripto == 2:
                # Abrindo o arquivo e lendo todas as linhas
                with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
                    linhas = bd_arquivos.readlines()

                encontrado = False
                # Procurando pelo CPF do usuário no arquivo
                for i in range(0, len(linhas), 7):  # Lendo quantas linhas tem em cada cadastro de usuário
                    if linhas[i].strip() == cpf_user_login and i + 6 < len(linhas):
                        saldo_ripple_bd = float(linhas[i + 5].split(":")[1])  # Saldo de Ripple do usuário

                        # Obtendo a cotação atual do Ripple
                        with open('cotacoes.txt', 'r') as bd_cotacoes:
                            cot = bd_cotacoes.readlines()
                        for c in cot:
                            moeda, valor = c.strip().split(':')
                            if moeda.lower() == 'ripple':
                                cot_ripple = float(valor)

                        # Calculando o valor total dos Ripples do usuário
                        valor_total_ripple = saldo_ripple_bd * cot_ripple

                        # Calculando o valor da venda em reais
                        valor_venda_reais = valor_venda_moeda * cot_ripple

                        # Calculando o valor da taxa de venda
                        taxa_venda = valor_venda_reais * 0.01  # Assumindo uma taxa de venda de 1%

                        if saldo_ripple_bd >= valor_venda_moeda:
                            novo_saldo_usuario = float(linhas[i + 3].split(":")[1]) + valor_venda_reais - taxa_venda

                            # Calculando o novo saldo de Ripple após a venda
                            novo_saldo_ripple = saldo_ripple_bd - valor_venda_moeda

                            # Atualizando o saldo em reais no arquivo
                            linhas[i + 3] = f"Reais:{novo_saldo_usuario:.2f}\n"

                            # Atualizando o saldo de Ripple no arquivo
                            linhas[i + 5] = f"Ripple:{novo_saldo_ripple:.4f}\n"

                            # Marcando como encontrado
                            encontrado = True

                            # Registrando a venda no extrato
                            now = datetime.now()
                            data_hora = now.strftime("%d-%m-%Y %H:%M")  # FORMATO (DD/MM/AAA HORA)

                            with open('bd_extrato.txt', 'a') as bd_extrato:
                                bd_extrato.write(f"{data_hora} - {valor_venda_moeda:.4f} XRP CT: 0.0   TX: {taxa_venda:.2f} REAL: {novo_saldo_usuario:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")
                                bd_extrato.write(f"{data_hora} + {valor_venda_reais:.2f} REAL CT: 0.0   TX: 0.00 REAL: {novo_saldo_usuario:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")

                            # Saindo do loop
                            break

                if encontrado:
                    # Escrevendo as linhas atualizadas no arquivo
                    with open('Bd_Usuarios.txt', 'w') as bd_arquivos:
                        bd_arquivos.writelines(linhas)

                    print("Venda de Ripple realizada com sucesso. Digite 1 para consultar seu saldo.")
                else:
                    print("Saldo insuficiente para realizar a venda de Ripple.")



########## ETHEREUM ########### ETHEREUM ################### ETHEREUM ########### ETHEREUM ########
            elif opcao_cripto == 3:
                # Abrindo o arquivo e lendo todas as linhas
                with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
                    linhas = bd_arquivos.readlines()

                encontrado = False
                # Procurando pelo CPF do usuário no arquivo
                for i in range(0, len(linhas), 7):  # Lendo quantas linhas tem em cada cadastro de usuário
                    if linhas[i].strip() == cpf_user_login and i + 6 < len(linhas):
                        saldo_ethereum_bd = float(linhas[i + 6].split(":")[1])  # Saldo de Ethereum do usuário

                        if saldo_ethereum_bd >= valor_venda_moeda:
                            # Obtendo a cotação atual do Ethereum
                            with open('cotacoes.txt', 'r') as bd_cotacoes:
                                cot = bd_cotacoes.readlines()
                            for c in cot:
                                moeda, valor = c.strip().split(':')
                                if moeda.lower() == 'ethereum':
                                    cot_ethereum = float(valor)

                            # Calculando o valor total da venda em reais
                            valor_venda_reais = valor_venda_moeda * cot_ethereum

                            # Calculando o valor da taxa de venda (2%)
                            taxa_venda = valor_venda_reais * 0.02

                            # Calculando o valor total da venda (descontando a taxa)
                            valor_total_venda = valor_venda_reais - taxa_venda

                            novo_saldo_usuario = float(linhas[i + 3].split(":")[1]) + valor_total_venda  # Calculando o novo saldo em reais
                            novo_saldo_ethereum = saldo_ethereum_bd - valor_venda_moeda  # Calculando o novo saldo de Ethereum

                            # Atualizando o saldo em reais no arquivo
                            linhas[i + 3] = f"Reais:{novo_saldo_usuario:.2f}\n"

                            # Atualizando o saldo de Ethereum no arquivo
                            linhas[i + 6] = f"Ethereum:{novo_saldo_ethereum:.4f}\n"

                            # Marcando como encontrado
                            encontrado = True

                            # Registrando a venda no extrato
                            now = datetime.now()
                            data_hora = now.strftime("%d-%m-%Y %H:%M")  # FORMATO (DD/MM/AAA HORA)

                            with open('bd_extrato.txt', 'a') as bd_extrato:
                                bd_extrato.write(f"{data_hora} - {valor_venda_moeda:.2f} ETH CT: 0.0    TX: {taxa_venda:.2f} REAL: {novo_saldo_usuario:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")
                                bd_extrato.write(f"{data_hora} + {valor_total_venda:.2f} REAL CT: 0.0    TX: 0.00 REAL: {novo_saldo_usuario:.2f} BTC: 0.0 ETH: 0.0 XRP: 0.0\n")

                            # Saindo do loop
                            break

                if encontrado:
                    # Escrevendo as linhas atualizadas no arquivo
                    with open('Bd_Usuarios.txt', 'w') as bd_arquivos:
                        bd_arquivos.writelines(linhas)

                    print("Venda de Ethereum realizada com sucesso. Digite 1 para consultar seu saldo.")
                else:
                    print("Saldo insuficiente para realizar a venda de Ethereum.")

# FUNÇÃO DE CONSULTAR EXTRATO POR USUARIO
def consultar_extrato(cpf_user_login):
    global nome_usuario
    senha_user_login = input("Digite a sua senha: ")

    with open('Bd_Usuarios.txt', 'r') as bd_arquivos:
        linhas = bd_arquivos.readlines()

    encontrado = False
    # Procurando pelo CPF do usuário no arquivo
    for i in range(0, len(linhas), 7):  # Avançando de 7 em 7 linhas para ver os dados de cada usuário
        if i + 6 < len(linhas):  # Verifica se o índice está dentro dos limites da lista
            if linhas[i].strip() == cpf_user_login and linhas[i + 1].strip() == senha_user_login:
                encontrado = True
                if encontrado:
                    with open('bd_extrato.txt', 'r') as bd_extr:
                        linhas = bd_extr.readlines()
                    extrato_usuario = []
                    for linha in linhas:
                        
                            extrato_usuario.append(linha.strip())

                    print("Extrato do usuário:")
                    print("")
                    print("Nome: ",nome_usuario)
                    print("Cpf: ",cpf_user_login)
                    print("")
                    for linha in extrato_usuario:
                        print(linha)
            else:
                print("")
                print("Sua senha esta incorreta, por favor, tente novamente")        

# FUNÇÃO DE ATUALIZAR COTAÇÃO
def atualizar_cotacoes():

    cotacoes_atualizadas = {}
    
    with open('cotacoes.txt', 'r') as file:
        for line in file:
            moeda, valor_anterior = line.strip().split(':')
            valor_anterior = float(valor_anterior)
            variacao_maxima = valor_anterior * 0.05
            nova_variacao = random.uniform(-variacao_maxima, variacao_maxima)
            novo_valor = valor_anterior + nova_variacao
            novo_valor = max(0.95 * valor_anterior, min(1.05 * valor_anterior, novo_valor))
            cotacoes_atualizadas[moeda] = novo_valor
          
    
    with open('cotacoes.txt', 'w') as file:
        for moeda, valor in cotacoes_atualizadas.items():
            file.write(f"{moeda}:{valor:.2f}\n")
           
    print("Cotações atualizadas com sucesso")
    return cotacoes_atualizadas
    

                

while True:
    print("")
    print("↓↓ Seja bem-vindo à principal central de investidores da FEINANCE. Selecione uma das opções abaixo: ↓↓")
    menu = [
        "1 -> Consultar Saldo",
        "2 -> Consultar Extrato",
        "3 -> Depositar",
        "4 -> Sacar",
        "5 -> Comprar Criptomoeda",
        "6 -> Vender Criptomoeda",
        "7 -> Atualizar Cotação",
        "8 -> Sair"
    ]
    for item in menu:
        print(item)
       
    opcao = int(input("Digite o número da opção desejada: ")) 
    print("                                                ")
    if opcao == 1:
        Consultar_saldo(cpf_user_login)
    elif opcao == 2:  
        consultar_extrato(cpf_user_login)
    elif opcao == 3:  
        Deposito(cpf_user_login)
    elif opcao == 4:  
        sacar_fundo(cpf_user_login)    
    elif opcao == 5:  
        Comprar_criptos(cpf_user_login) 
    elif opcao == 6:  
        vender_cripto(cpf_user_login)
    elif opcao == 7:  
        atualizar_cotacoes()    
    elif opcao == 8:  
        print("Muito obrigado por usar o FEINANCE. Até a próxima.")
        break 
    else:    
        print("Digite uma opção válida")
