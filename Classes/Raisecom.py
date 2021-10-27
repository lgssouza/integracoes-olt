from flask import Flask, request, jsonify
import json
import time
import sys
import telnetlib
import os


class Raisecom():
    #Método que realzia a conexao via telnet 
    @staticmethod
    def conexao(ip_olt, porta_telnet, usuario_olt, senha_olt):
        global telnet
        #Envia parâmetros necessários para entrar no modo de configuração Raisecom
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
        script_busca_onu = 'show interface gpon-olt illegal'
        telnet.write(script_busca_onu.encode('utf-8')+b"\n")
        telnet.write(b'exit\nexit\n')
        time.sleep(2)      
        data = telnet.read_all()
        data = data.decode('ISO-8859-1')
        data = data.lstrip()
        print(data)
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
        return data_json
    
    def desautorizaOnu(slot_pon, id_onu):
        resposta    = []
        telnet.read_until(b"Raisecom#")
        telnet.write(b"config\n")
        telnet.read_until(b"Raisecom(config)#")
        script_abrir_interface = 'interface gpon-olt '+slot_pon
        telnet.write(script_abrir_interface.encode('utf-8')+b"\n")
        script_exclusao_onu = 'no create gpon-onu '+id_onu
        telnet.write(script_exclusao_onu.encode('utf-8')+b"\n")
        telnet.write(b'exit\nexit\nexit\nexit\n')
        time.sleep(2)
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
        return data_json

    def consultaSinalOnu(id_onu):
        resposta    = [] 
        script_consulta_sinal_onu = 'show gpon-onu '+ id_onu +' transceiver'
        telnet.write(script_consulta_sinal_onu.encode('utf-8')+b"\n")
        telnet.write(b'exit\nexit\n')
        time.sleep(2)
        #Recebe os dados retornado
        data = telnet.read_all()
        data = data.decode('ISO-8859-1')
        data = data.lstrip()
        print(data)
        for linha in data.split("\n"):
            #separada cada elementos da linha colocando como elemento de uma lista
            elementos = linha.rstrip().split(" ")
            #Caso a quantidade de elementos seja maior que 4, é a linha que contem as informações da(s) onu(s)
            if len(elementos) > 4 and elementos[0] != "ONU":
                dados_onu = {
                    "SINAL": elementos[-1]
                }
                #insere o conjunto dentro do array de resposta
                #Dessa forma, caso tenha mais de uma ONU, todas serão enviadas via json
                resposta.append(dados_onu)
        #Convertendo um dicionário criado em um json
        data_json = json.dumps(resposta)
        return data_json

    def relatorioSinaisOnus(ip_olt, porta_telnet, usuario_olt, senha_olt, slot_pon):
        resposta    = [] 
        #Percorre cada slot cadastrado
        for linha in slot_pon:
            pon=int(linha['pon'])
            #Percorre cada pon do slot, para averiguar o sinal de cada onu
            while(pon <= int(linha['pon'])):
                #Realiza uma nova conexão em cada consulta
                Raisecom.conexao(ip_olt, porta_telnet, usuario_olt, senha_olt)
                time.sleep(1)
                #remove a paginacao do terminal telnet
                telnet.write(b"terminal page-break disable\n")
                #script de consulta no slot correspondente ao for, passando portodas pons desse slot
                script_consulta_sinal_pon = 'show interface gpon-olt '+linha['slot']+'/'+str(pon)+' transceiver rx-onu-power'
                telnet.write(script_consulta_sinal_pon.encode('utf-8')+b"\n")
                #envia mensagens de quebra de linha para trazer todos resultados
                telnet.write(b"  \r\n")
                telnet.write(b"  \r\n")
                telnet.write(b"  \r\n")
                telnet.write(b'exit\nexit\n')
                time.sleep(1)
                #Recebe os dados retornado
                data = telnet.read_all()
                data = data.decode('ISO-8859-1')
                data = data.lstrip()
                telnet.close()
                for linha_onu in data.split("\n"):
                    #verifica se a linha analisada contem "More", para que seja tratado
                    if "More" in linha_onu:
                        linha_onu = linha_onu.replace("\x08","").replace("--More--","")
                        linha_onu = linha_onu.lstrip()
                    #separada cada elementos da linha colocando como elemento de uma lista
                    elementos = linha_onu.split(" ")
                    #Caso a quantidade de elementos seja maior que 4, é a linha que contem as informações da(s) onu(s)
                    if len(elementos) > 4 and elementos[0] != "ONU" and elementos[0] != "Raisecom#show":
                        dados_onu = {
                            "ONU_ID": elementos[0],
                            "SINAL": elementos[-8],
                        }
                        #insere o conjunto dentro do array de resposta
                        #Dessa forma, caso tenha mais de uma ONU, todas serão enviadas via json
                        resposta.append(dados_onu)
                pon += 1   
        data_json = json.dumps(resposta)
        print(data_json)
        return data_json
