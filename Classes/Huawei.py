from flask import Flask, request, jsonify
import json
import time
import sys
import telnetlib
import os


class Huawei():
    #Método que realzia a conexao via telnet 
    @staticmethod
    def conexao(ip_olt, porta_telnet, usuario_olt, senha_olt):
        global telnet
        #Envia parâmetros necessários para entrar no modo de configuração Huawei
        telnet = telnetlib.Telnet()
        telnet.open(ip_olt,porta_telnet,25)
        telnet.read_until(b"Login:")
        telnet.write(usuario_olt.encode('utf-8')+b"\n")
        telnet.read_until(b"Password:")
        telnet.write(senha_olt.encode('utf-8')+b"\n")
        telnet.write(b"ena\n")
        telnet.read_until(b"Password:")
        telnet.write(senha_olt.encode('utf-8')+b"\n")
    
    def buscaOnu():
        resposta    = [] 
        telnet.write(b'enable\n')
        acesso_terminal = 'configure terminal'
        telnet.write(acesso_terminal.encode('utf-8')+b"\n")
        script_busca_onu = 'display ont autofind all'
        telnet.write(script_busca_onu.encode('utf-8')+b"\n")
        time.sleep(2)      
        data = telnet.read_all()
        data = data.decode('ISO-8859-1')
        data = data.lstrip()
        print(data)
        '''
        for linha in data.split("\n"):
            linha = linha.replace("\t"," ")
            linha = linha.replace("\r","")
            #separada cada elementos da linha colocando como elemento de uma lista
            elementos = linha.split(" ")
            #Caso a quantidade de elementos seja maior que 7, é a linha que contem as informações da(s) onu(s)
            if len(elementos) > 7 and not(elementos[0] == "OLT"):
                slot_pon = elementos[0].split("/")
                dados_onu = {
                    "SLOT": slot_pon[0],
                    "PON": slot_pon[1],
                    "MAC": elementos[12],
                    "TIPO_ONU": '-'
                }
                #insere o conjunto dentro do array de resposta
                #Dessa forma, caso tenha mais de uma ONU, todas serão enviadas via json
                resposta.append(dados_onu)
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta)  
        '''
        return 'data_json'

    def autorizaOnu(numero_pon, mac_onu, nome_cliente, vlan, onu_id):
        resposta    = [] 
        slot_pon = numero_pon.split("/")
        telnet.write(b'enable\n')
        acesso_terminal = 'configure terminal'
        telnet.write(acesso_terminal.encode('utf-8')+b"\n")
        script_interface = 'interface'+numero_pon
        telnet.write(script_interface.encode('utf-8')+b"\n")
        script_liberacao = 'ont add '+slot_pon[1]+ ' sn-auth '+ mac_onu + 'omci ont-lineprofile-id 1 ont-srvprofile-id 1 desc '+nome_cliente
        telnet.write(script_liberacao.encode('utf-8')+b"\n")
        script_vlan = 'ont port native-vlan '+slot_pon[1]+ ' '+ onu_id + 'eth 1 vlan '+ vlan
        telnet.write(script_vlan.encode('utf-8')+b"\n")

        '''
            Script de criar serviço
        '''
        time.sleep(2)      
        data = telnet.read_all()
        data = data.decode('ISO-8859-1')
        data = data.lstrip()
        print(data)
        '''
        #script_liberacao_onu = script_liberacao_onu.encode('utf-8')
        #Envia os dados via sendall, metodo do socket, todo codificado em uma cadeia de strings em UTF-8
        try:
            telnet.settimeout(15)
            print(telnet.gettimeout())
            telnet.sendall(script_liberacao_onu.encode('utf-8'))
            time.sleep(2)
        except:
            print("entrou no except")
            Huawei.logout()
        #Recebe os dados retornado
        data = telnet.recv(1024)
        #decodifica esses dados de bytes para uma cadeia de strings UTF-8
        data = data.decode("utf-8")
        #data = data.replace(" ","")
        for linha in data.split("\n"):
            #indentifica dentro da linha, qual contem a resposta da requisição (ENDESC)
            if "ENDESC" in linha:
                #Quebra o conteudo da linha e faz com que cada parte separada por igual seja um elemento da lista
                elemento = linha.split("=")
                resp = Huawei.retornaResposta(elemento[2])
                break
        #Percorre todas linhas de retorno, separando cada uma delas como elementos de uma lista onde existe quebra de linha
        mensagem = {
            "msg": resp
        }  
        resposta.append(mensagem)
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta)  
        #telnet.shutdown(socket.SHUT_RDWR)
        #telnet.close()
        '''
        return 'data_json'
    
    def desautorizaOnu(numero_pon, onu_id):
        resposta    = [] 
        slot_pon = numero_pon.split("/")
        telnet.write(b'enable\n')
        acesso_terminal = 'configure terminal'
        telnet.write(acesso_terminal.encode('utf-8')+b"\n")
        script_interface = 'interface'+numero_pon
        telnet.write(script_interface.encode('utf-8')+b"\n")
        script_desautorizacao = 'ont delete '+slot_pon[1]+ ' '+ onu_id
        telnet.write(script_desautorizacao.encode('utf-8')+b"\n")
        time.sleep(2)      
        data = telnet.read_all()
        data = data.decode('ISO-8859-1')
        data = data.lstrip()
        print(data)
        '''
        #Recebe os dados retornado
        data = telnet.read_all()
        data = data.decode('ISO-8859-1')
        for linha in data.split("\n"):
            #indentifica dentro da linha, qual contem a resposta da requisição (ENDESC)
            if "successfully" in linha:
                resp = "Sucesso"
        #Percorre todas linhas de retorno, separando cada uma delas como elementos de uma lista onde existe quebra de linha
        mensagem = {
            "msg": resp
        }
        resposta.append(mensagem)
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta) 
        '''
        return 'data_json'

    def consultaSinalOnu(numero_pon, onu_id):
        resposta    = [] 
        slot_pon = numero_pon.split("/")
        telnet.write(b'enable\n')
        acesso_terminal = 'configure terminal'
        telnet.write(acesso_terminal.encode('utf-8')+b"\n")
        script_interface = 'interface'+numero_pon
        telnet.write(script_interface.encode('utf-8')+b"\n")
        script_consulta_sinal = 'display optical-info ont '+slot_pon[1]+ ' '+ onu_id
        telnet.write(script_consulta_sinal.encode('utf-8')+b"\n")
        time.sleep(2)      
        data = telnet.read_all()
        data = data.decode('ISO-8859-1')
        data = data.lstrip()
        print(data)
        '''
        #Recebe os dados retornado
        data = telnet.read_all()
        data = data.decode('ISO-8859-1')
        for linha in data.split("\n"):
            #indentifica dentro da linha, qual contem a resposta da requisição (ENDESC)
            if "successfully" in linha:
                resp = "Sucesso"
        #Percorre todas linhas de retorno, separando cada uma delas como elementos de uma lista onde existe quebra de linha
        mensagem = {
            "msg": resp
        }
        resposta.append(mensagem)
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta) 
        '''
        return 'data_json'
