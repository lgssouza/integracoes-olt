from flask import Flask, request, jsonify
import json
import time
import sys
import socket 
#modulo que executa a conexão via ssh
#import paramiko
#importa a classe com os métodos da Fiberhome
from Classes.Fiberhome import Fiberhome
#importa a classe com os métodos da Raisecom
from Classes.Raisecom import Raisecom
#importa a classe com os métodos da Huawei
from Classes.Huawei import Huawei
#importa a classe com os métodos da Huawei TL1
from Classes.HuaweiTL1 import HuaweiTL1

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "<h1 style='color:purple'>TL Software</h1>"

#Método que busca as ONUs não autorizadas
@app.route("/buscaOnu", methods=['POST'])
def buscaOnu():
    #Recebe as informações em json de conexão via POST
    dados_olt = request.json
    #identifica o fabricante, para utilizar os métodos corretos
    if dados_olt['fabricante'] == 'FIBERHOME':
        #utiliza o método de conexão Fiberhome, passando os dados recebidos via post
        Fiberhome.conexao(dados_olt['ip_servidor_tl1'], int(dados_olt['porta_servidor_tl1']), dados_olt['usuario_anm'], dados_olt['senha_anm'])
        #retorna as onus não aurotizadas
        return Fiberhome.buscaOnu(dados_olt['ip_olt'])
    elif dados_olt['fabricante'] == 'RAISECOM':
        Raisecom.conexao(dados_olt['ip_olt'], int(dados_olt['porta_telnet']), dados_olt['usuario_olt'], dados_olt['senha_olt'])
        return Raisecom.buscaOnu()
    elif dados_olt['fabricante'] == 'HUAWEI':
        Huawei.conexao(dados_olt['ip_olt'], int(dados_olt['porta_telnet']), dados_olt['usuario_olt'], dados_olt['senha_olt'])
        return Huawei.buscaOnu()
    elif dados_olt['fabricante'] == 'HUAWEI_TL1':
        HuaweiTL1.conexao(dados_olt['ip_servidor_tl1'], int(dados_olt['porta_servidor_tl1']), dados_olt['usuario_u2000'], dados_olt['senha_u2000'])
        return HuaweiTL1.buscaOnu(dados_olt['ip_olt'])

@app.route("/autorizaOnu", methods=['POST'])
def autorizaOnu():
    #Recebe as informações em json de conexão via POST
    dados = request.json
    #identifica o fabricante, para utilizar os métodos corretos
    if dados['fabricante'] == 'FIBERHOME':
        Fiberhome.conexao(dados['ip_servidor_tl1'], int(dados['porta_servidor_tl1']), dados['usuario_anm'], dados['senha_anm'])
        #utiliza o método de autorização Fiberhome, passando os dados recebidos via post
        return Fiberhome.autorizaOnu(dados['ip_olt'],dados['numero_pon'],dados['mac_onu'],dados['tipo_onu'],dados['nome_cliente'],dados['vlan'])
    elif dados['fabricante'] == 'HUAWEI':
        Huawei.conexao(dados['ip_olt'], int(dados['porta_telnet']), dados['usuario_olt'], dados['senha_olt'])
        return Huawei.autorizaOnu(dados['numero_pon'],dados['mac_onu'],dados['tipo_onu'],dados['nome_cliente'],dados['vlan'])
    elif dados['fabricante'] == 'HUAWEI_TL1':
        HuaweiTL1.conexao(dados['ip_servidor_tl1'], int(dados['porta_servidor_tl1']), dados['usuario_u2000'], dados['senha_u2000'])
        return HuaweiTL1.autorizaOnu(dados['ip_olt'],dados['slot'],dados['pon'],dados['mac_onu'],dados['nome_cliente'],dados['vlan'])

@app.route("/desautorizaOnu", methods=['POST'])
def desautorizaOnu():
    #Recebe as informações em json de conexão via POST
    dados = request.json
    #identifica o fabricante, para utilizar os métodos corretos
    if dados['fabricante'] == 'FIBERHOME':
        #utiliza o método de conexão Fiberhome, passando os dados recebidos via post
        Fiberhome.conexao(dados['ip_servidor_tl1'], int(dados['porta_servidor_tl1']), dados['usuario_anm'], dados['senha_anm'])
        return Fiberhome.desautorizaOnu(dados['ip_olt'],dados['mac_onu'],dados['slot_pon'])
    elif dados['fabricante'] == 'RAISECOM':
        Raisecom.conexao(dados['ip_olt'], int(dados['porta_telnet']), dados['usuario_olt'], dados['senha_olt'])
        return Raisecom.desautorizaOnu(dados['slot_pon'],dados['id_onu'])
    elif dados['fabricante'] == 'HUAWEI':
        Huawei.conexao(dados['ip_olt'], int(dados['porta_telnet']), dados['usuario_olt'], dados['senha_olt'])
        return Huawei.desautorizaOnu(dados['numero_pon'],dados['id_onu'])
    elif dados['fabricante'] == 'HUAWEI_TL1':
        HuaweiTL1.conexao(dados['ip_servidor_tl1'], int(dados['porta_servidor_tl1']), dados['usuario_u2000'], dados['senha_u2000'])
        return HuaweiTL1.desautorizaOnu(dados['ip_olt'],dados['slot'],dados['pon'],dados['id_onu'])

@app.route("/consultaSinalOnu", methods=['POST'])
def consultaSinalOnu():
    #Recebe as informações em json de conexão via POST
    dados = request.json
    #identifica o fabricante, para utilizar os métodos corretos
    if dados['fabricante'] == 'FIBERHOME':
        #utiliza o método de conexão Fiberhome, passando os dados recebidos via post
        Fiberhome.conexao(dados['ip_servidor_tl1'], int(dados['porta_servidor_tl1']), dados['usuario_anm'], dados['senha_anm'])
        return Fiberhome.consultaSinalOnu(dados['ip_olt'],dados['mac_onu'],dados['slot_pon'])
    elif dados['fabricante'] == 'RAISECOM':
        Raisecom.conexao(dados['ip_olt'], int(dados['porta_telnet']), dados['usuario_olt'], dados['senha_olt'])
        return Raisecom.consultaSinalOnu(dados['id_onu'])
    elif dados['fabricante'] == 'HUAWEI':
        Huawei.conexao(dados['ip_olt'], int(dados['porta_telnet']), dados['usuario_olt'], dados['senha_olt'])
        return Huawei.consultaSinalOnu(dados['numero_pon'],dados['id_onu'])
    elif dados['fabricante'] == 'HUAWEI_TL1':
        HuaweiTL1.conexao(dados['ip_servidor_tl1'], int(dados['porta_servidor_tl1']), dados['usuario_u2000'], dados['senha_u2000'])
        return HuaweiTL1.consultaSinalOnu(dados['ip_olt'],dados['slot'],dados['pon'],dados['id_onu'])

@app.route("/relatorioSinaisOnus", methods=['POST'])
def relatorioSinaisOnus():
    #Recebe as informações em json de conexão via POST
    dados = request.json
    #identifica o fabricante, para utilizar os métodos corretos
    if dados['fabricante'] == 'FIBERHOME':
        #utiliza o método de conexão Fiberhome, passando os dados recebidos via post
        Fiberhome.conexao(dados['ip_servidor_tl1'], int(dados['porta_servidor_tl1']), dados['usuario_anm'], dados['senha_anm'])
        return Fiberhome.relatorioSinaisOnus(dados['ip_olt'],dados['mac_onu'],dados['slot_pon'])
    elif dados['fabricante'] == 'RAISECOM':
        return Raisecom.relatorioSinaisOnus(dados['ip_olt'], int(dados['porta_telnet']), dados['usuario_olt'], dados['senha_olt'],dados['slot_pon'])

@app.route("/desautorizaONUPon", methods=['POST'])
def desautorizaONUPon():
    #Recebe as informações em json de conexão via POST
    dados = request.json
    #identifica o fabricante, para utilizar os métodos corretos
    if dados['fabricante'] == 'FIBERHOME':
        #utiliza o método de conexão Fiberhome, passando os dados recebidos via post
        Fiberhome.conexao(dados['ip_servidor_tl1'], int(dados['porta_servidor_tl1']), dados['usuario_anm'], dados['senha_anm'])
        return Fiberhome.desautorizaONUPon(dados['ip_olt'],dados['clientes'])

@app.route("/atualizaONUPon", methods=['POST'])
def atualizaONUPon():
    #Recebe as informações em json de conexão via POST
    dados = request.json
    #identifica o fabricante, para utilizar os métodos corretos
    if dados['fabricante'] == 'FIBERHOME':
        #utiliza o método de conexão Fiberhome, passando os dados recebidos via post
        Fiberhome.conexao(dados['ip_servidor_tl1'], int(dados['porta_servidor_tl1']), dados['usuario_anm'], dados['senha_anm'])
        return Fiberhome.atualizaONUPon(dados['ip_olt'],dados['clientes'])

@app.route("/derrubaCliente", methods=['POST'])
def derrubaCliente():
    dados = request.json
    #return dados
    """
    host = "68.183.8.21"
    port = 22022
    username = "root"
    password = 'pLasqMFY!uPU'

    command = "ls"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(host, port, username)
    ssh.connect(host, port, username, password)


    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    print(lines)"""
    #cria a instância do ssh client
    ssh = paramiko.SSHClient()

    #determina que a conexão será a partir de uma chave ssh ja conhecida pelo servidor
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(dados['ip_servidor'], 22022, username=dados['usuario'], password=dados['senha'])

    command = "echo 'Acct-Session-Id="+dados['acctsessionid']+"' | radclient -t 0 "+dados['nasipaddress']+":3799 'disconnect' q0El49TG"
    command = "".join("echo 'Acct-Session-Id=", dados['acctsessionid'],"' | radclient -t 0 ", dados['nasipaddress'], ":3799 'disconnect' q0El49TG")
    #command = "echo 'User-Name="+dados['usuario_pppoe']+"' | radclient -t 0 "+dados['nasipaddress']+":3799 'disconnect' q0El49TG"
    stdin, stdout, stderr = ssh.exec_command(command)

    print(stdout.readlines())

    ssh.close()
    print(dados)
    print(command)
    return "ok"

#app.run()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
