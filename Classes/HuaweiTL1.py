from flask import Flask, request, jsonify
import json
import time
import sys
import socket 

class HuaweiTL1():
    #Método que interpreta a resposta recebida e devolve a mensagem para ser enviada via json
    @staticmethod
    def retornaResposta(resposta):
        if "resource does not exist" in resposta:
            return "O dispositivo não existe"
        elif "the alarm does not exist" in resposta:
            return "O alarme não existe"
        elif "missing parameter" in resposta:
            return "Ausência de parâmetro"
        elif "invalid parameter format" in resposta:
            return "Formato de parâmetro inválido"
        elif "input parameter error" in resposta:
            return "Parâmetro de entrada inválido"
        elif "device may not support this operation" in resposta:
            return "O dispositivo pode não suportar esta operação"
        elif "device operation failed" in resposta:
            return "A operação no dispositivo falhou"
        elif "device is busy" in resposta:
            return "O dispositivo está ocupado"
        elif "EMS may not support this operation" in resposta:
            return "O EMS pode não suportar esta operação"
        elif "EMS operation failed" in resposta:
            return "Falha na operação do EMS"
        elif "EMS exception happens" in resposta:
            return "Aconteceu uma exceção no EMS"
        elif "user is busy" in resposta:
            return "O usuário está ocupado"
        elif "user is testing" in resposta:
            return "O usuário está em teste"
        elif "test module is busy" in resposta:
            return "O módulo de teste está ocupado"
        elif "resource already exist" in resposta:
            return "O nome ja existe"
        elif "No error" in resposta:
            return "Sucesso"
        else:
            return "Erro"
    #Método que realzia a conexao via TL1 
    def conexao(ip_servidor_tl1, porta_servidor_tl1, usuario_anm, senha_anm):
        global conexao
        #AF_INET informa que será usado o  procolo TCP
        #SOCK_STREAM informa que será usado IPV4 na conexão
        conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conexao.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tmp = conexao.connect_ex((ip_servidor_tl1, porta_servidor_tl1))
        #Usuário e senha do anm/unm
        script_conexao = 'LOGIN:::CTAG::UN='+usuario_anm+',PWD='+senha_anm+';'
        script_conexao = script_conexao.encode('utf-8')
        #script_handshake = 'SHAKEHAND:::CTAG::;'
        conexao.send(script_conexao)
        #conexao.sendall(script_handshake.encode('utf-8'))
        time.sleep(2)

    @staticmethod
    def logout():
        script_logout = 'LOGOUT:::CTAG::;'
        script_logout = script_logout.encode('utf-8')
        conexao.send(script_logout)
        time.sleep(2)
        conexao.shutdown(1)
        time.sleep(2)
        conexao.close()

    def buscaOnu(ip_olt):
        resposta    = [] 
        oltip   = ip_olt
        script_busca_onu = 'LST-GPONONTAUTOFIND::DEV='+oltip+'::;'
        conexao.settimeout(15)
        conexao.sendall(script_busca_onu.encode('utf-8'))
        time.sleep(2)
        data = conexao.recv(5000)
        data = data.decode("ISO-8859-1")
        data = data.replace(" ","")
        print(data)
        """ for linha in data.split("\n"):
            linha = linha.replace("\t"," ")
            linha = linha.replace("\r","")
            #separada cada elementos da linha colocando como elemento de uma lista
            elementos = linha.split(" ")
            #Caso a quantidade de elementos seja maior que 7, é a linha que contem as informações da(s) onu(s)
            if len(elementos) > 7 and not(elementos[0] == "SLOTNO"):
                dados_onu = {
                    "SLOT": elementos[0],
                    "PON": elementos[1],
                    "MAC": elementos[2][0:12],
                    "TIPO_ONU": elementos[7]
                }
                #insere o conjunto dentro do array de resposta
                #Dessa forma, caso tenha mais de uma ONU, todas serão enviadas via json
                resposta.append(dados_onu)
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta)  
        HuaweiTL1.logout() """
        return 'data_json'

    def autorizaOnu(ip_olt, slot, pon, mac_onu, nome_cliente, vlan):
        resposta    = [] 
        script_liberacao_onu = 'ADD-ONT::DEV='+ip_olt+',SN='+slot+',PN='+pon+'::NAME='+nome_cliente+',SERIALNUM='+mac_onu+',AUTH=S,RETURNONTID=TRUE;'
        conexao.settimeout(15)
        conexao.sendall(script_liberacao_onu.encode('utf-8'))
        time.sleep(2)
        data = conexao.recv(1024)
        data = data.decode("utf-8")
        print(data)

        '''Depois de pegar o retorno do comando add, utiliza o ont id para adiicionar uma VLAN'''
        script_liberacao_vlan = 'CFG-ONTVLAN::DEV='+ip_olt+',SN='+slot+',PN='+pon+',ONTID-'+ontid+':CTAG::WANVLAN='+vlan+';'


        """ for linha in data.split("\n"):
            #indentifica dentro da linha, qual contem a resposta da requisição (ENDESC)
            if "ENDESC" in linha:
                #Quebra o conteudo da linha e faz com que cada parte separada por igual seja um elemento da lista
                elemento = linha.split("=")
                resp = HuaweiTL1.retornaResposta(elemento[2])
                break
        #Percorre todas linhas de retorno, separando cada uma delas como elementos de uma lista onde existe quebra de linha
        mensagem = {
            "msg": resp
        }  
        resposta.append(mensagem)
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta)   
        HuaweiTL1.logout() """
        return 'data_json'

    def desautorizaOnu(ip_olt, slot, pon, id_onu):
        resposta    = [] 
        script_exclusao_onu = 'DEL-ONT::DEV='+ip_olt+',SN='+slot+',PN='+pon+',ONTID-'+id_onu+',DELCONFIG=TRUE:1::;'

        conexao.settimeout(15)
        conexao.sendall(script_exclusao_onu.encode('utf-8'))
        time.sleep(2)
        data = conexao.recv(1024)
        data = data.decode("utf-8")
        print(data)
        """ for linha in data.split("\n"):
            #indentifica dentro da linha, qual contem a resposta da requisição (ENDESC)
            if "ENDESC" in linha:
                #Quebra o conteudo da linha e faz com que cada parte separada por igual(=) seja um elemento da lista
                elemento = linha.split("=")
                #a posição 2 da lista de elementos é a resposta
                #a resposta é passa para a função retornaResposta, que verifica a mensagem, e retorna a resposta que será enviada no json
                resp = HuaweiTL1.retornaResposta(elemento[2])
        #Percorre todas linhas de retorno, separando cada uma delas como elementos de uma lista onde existe quebra de linha
        mensagem = {
            "msg": resp
        }
        resposta.append(mensagem)
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta)  
        HuaweiTL1.logout() """
        return 'data_json'

    def consultaSinalOnu(ip_olt, slot, pon, id_onu):
        resposta    = []
        script_consulta_sinal_onu = 'LST-ONTDDMDETAIL::DEV='+ip_olt+',SN='+slot+',PN='+pon+',ONTID-'+id_onu+':CTAG::SHOWOPTION=OPTICSRXPOWERbyOLT;'

        conexao.settimeout(15)
        conexao.sendall(script_consulta_sinal_onu.encode('utf-8'))
        time.sleep(2)
        data = conexao.recv(1024)
        data = data.decode("utf-8")
        print(data)
        """ for linha in data.split("\n"):
            #indentifica dentro da linha, qual contem a resposta da requisição (ENDESC)
            if "IRNE" in linha:
                #Quebra o conteudo da linha e faz com que cada parte separada por igual(=) seja um elemento da lista
                elemento = linha.split("=")
                #a posição 2 da lista de elementos é a resposta
                #a resposta é passa para a função retornaResposta, que verifica a mensagem, e retorna a resposta que será enviada no json
                resp = HuaweiTL1.retornaResposta(elemento[2])
                mensagem = {
                    "msg": resp
                }
                resposta.append(mensagem)
        data = data.replace(" ","")
        #Percorre todas linhas de retorno, separando cada uma delas como elementos de uma lista onde existe quebra de linha
        for linha in data.split("\n"):
            linha = linha.replace("\t"," ")
            linha = linha.replace("\r","")
            #separada cada elementos da linha colocando como elemento de uma lista
            elementos = linha.split(" ")
            #Caso a quantidade de elementos seja maior que 7, é a linha que contem as informações da onu
            if len(elementos) > 7 and not(elementos[0] == "ONUID"):
                dados_onu = {
                    "SINAL": elementos[1]
                }
                #insere o conjunto dentro do array de resposta
                #Dessa forma, caso tenha mais de uma ONU, todas serão enviadas via json
                resposta.append(dados_onu)
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta)
        HuaweiTL1.logout() """
        return 'data_json'

    def desautorizaONUPon(ip_olt, clientes):
        cont_sucesso = 0
        resposta    = [] 
        #Percorre todos os clientes para desautorizar a ONU
        for cliente in clientes:
            #Cria variável que recebe a resposta da requisição
            resp_desautoriza = "inicio"
            #Executa o comando enquanto o retorno for diferente de "Sucesso"
            #Dessa maneira, se der erro, executará novamente
            while (resp_desautoriza != "Sucesso"):
                script_exclusao_onu = 'DEL-ONU::OLTID='+ip_olt+',PONID=NA-NA-'+cliente['slot_pon']+':CTAG::ONUIDTYPE=MAC,ONUID='+cliente['physical_address']+';'
                conexao.settimeout(15)
                conexao.sendall(script_exclusao_onu.encode('utf-8'))
                time.sleep(2)
                data = conexao.recv(1024)
                data = data.decode("utf-8")
                for linha in data.split("\n"):
                    if "ENDESC" in linha:
                        elemento = linha.split("=")
                        resp_desautoriza = HuaweiTL1.retornaResposta(elemento[2])
                        #Se a resposta for sucesso, sai do loop de desautorização
                        if(resp_desautoriza == "Sucesso"):
                            print(resp_desautoriza)
                            cont_sucesso = cont_sucesso + 1
                            break
        if (len(clientes) == cont_sucesso):
            resposta_delete = "Sucesso"
        else:
            resposta_delete = "Erro"
        mensagem = {
            "msg": resposta_delete,
            "qtd_registros": cont_sucesso
        }
        resposta.append(mensagem)
        data_json = json.dumps(resposta)  
        HuaweiTL1.logout()
        return data_json    

    def autorizaONUPon(ip_olt, clientes):
        resposta    = [] 
        script_busca_onu = 'LST-UNREGONU::OLTID='+ip_olt+':CTAG::;'
        conexao.settimeout(30)
        conexao.sendall(script_busca_onu.encode('utf-8'))
        time.sleep(2)
        #Recebe os dados retornado
        data = conexao.recv(5000)
        #decodifica esses dados de bytes para uma cadeia de strings UTF-8
        data = data.decode("ISO-8859-1'")
        print(data)
        data = data.replace(" ","")
        #Percorre todas linhas de retorno, separando cada uma delas como elementos de uma lista onde existe quebra de linha
        for linha in data.split("\n"):
            resp_autoriza = "inicio"
            linha = linha.replace("\t"," ")
            linha = linha.replace("\r","")
            #separada cada elementos da linha colocando como elemento de uma lista
            elementos = linha.split(" ")
            #Caso a quantidade de elementos seja maior que 7, é a linha que contem as informações da(s) onu(s)
            if len(elementos) > 7 and not(elementos[0] == "SLOTNO"):

                physical_address = elementos[2][0:12]
                print(physical_address)
                for cliente in clientes:
                    if(physical_address == cliente['physical_address']):
                        tipo_onu = elementos[7]
                        slot = elementos[0]
                        pon  = elementos[1]

                        if len(pon) < 2:
                            pon = "0"+pon
                        if len(slot) < 2:
                            slot = "0"+slot

                        if slot == "01":
                            vlan = "10"+pon
                        elif slot == "02":
                            vlan =  "20"+pon

                        numero_pon = slot+"-"+pon
                        while (resp_autoriza != "Sucesso"):
                            time.sleep(2)
                            script_liberacao_onu = 'ADD-ONU::OLTID='+ip_olt+',PONID=NA-NA-'+numero_pon+':CTAG::AUTHTYPE=MAC,ONUID='+physical_address+',NAME='+cliente['nome']+',ONUTYPE='+tipo_onu+';CFG-LANPORTVLAN::OLTID='+ip_olt+',PONID=NA-9-'+numero_pon+',ONUIDTYPE=MAC,ONUID='+physical_address+',ONUPORT=NA-NA-NA-1:CTAG::CVLAN='+vlan+';'
                            conexao.settimeout(30)
                            conexao.sendall(script_liberacao_onu.encode('utf-8'))
                            time.sleep(2)

                            data = conexao.recv(1024)
                            data = data.decode("utf-8")
                            for linha in data.split("\n"):

                                if "ENDESC" in linha:
                                    elemento = linha.split("=")
                                    resp_autoriza = HuaweiTL1.retornaResposta(elemento[2])
                                    if resp_autoriza == "Sucesso":
                                        print("liberacao: "+resp_autoriza)
                                        physical_address_retorno = numero_pon+" "+physical_address
                                        id_ip = cliente['id_ip']
                                        mensagem = {
                                            "physical_address": physical_address_retorno,
                                            "id_ip": id_ip
                                        }
                                        resposta.append(mensagem)
                                        break
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta)  
        HuaweiTL1.logout()
        return data_json   

    def atualizaONUPon(ip_olt, clientes):
        resposta    = [] 
        atualizado  = 0
        conexao.settimeout(30)
        for cliente in clientes:
            physical_address = cliente['physical_address']
            time.sleep(2)
            script_liberacao_onu = 'QUERY-ONUINFO::OLTID='+ip_olt+',PONID=NA-NA-NA-NA,ONUIDTYPE=MAC,ONUID='+physical_address+':CTAG::;'
            conexao.sendall(script_liberacao_onu.encode('utf-8'))
            time.sleep(2)

            data = conexao.recv(1024)
            data = data.decode("utf-8")
            for linha in data.split("\n"):
                if "SAO" in linha:
                    elemento = linha.replace(" ","")
                    elemento = elemento.split("\t")

                    slot = elemento[3]
                    pon  = elemento[4]

                    if len(slot) < 2:
                        slot = "0"+slot
                    if len(pon) < 2:
                        pon = "0"+pon
                    numero_pon = slot+"-"+pon
                    physical_address_retorno = numero_pon+" "+physical_address

                    script_atualizacao_nome = 'CFG-ONUNAMEANDDESC::OLTID='+ip_olt+',PONID=NA-NA-'+numero_pon+',ONUIDTYPE=MAC,ONUID='+physical_address+':CTAG::ONUNAME='+cliente['nome']+';'
                    conexao.sendall(script_atualizacao_nome.encode('utf-8'))
                    time.sleep(2)

                    id_ip = cliente['id_ip']
                    mensagem = {
                        "physical_address": physical_address_retorno,
                        "id_ip": id_ip
                    }
                    resposta.append(mensagem)
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta) 
        print(resposta)
        HuaweiTL1.logout() 
        return data_json 
