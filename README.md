# OpenOLT

O OpenOLT é uma biblioteca de código aberto para integração de OLT, um equipamentos utilizados por provedores de internet
para transmitir sinal óptico. meio de pagamento muito comum no Brasil. O foco é ser simples e ter uma arquitetura compatível com os recursos mais modernos do PHP.

## Instalação
Em breve...

## Consultando Onu

Essa é a melhor parte. Não poderia ser mais simples, veja um exemplo básico:

```php
POST /autorizaOnu HTTP/1.1
Host: yourhost.com
Content-Type: application/json
Content-Length: 342

{
    "ip_servidor_tl1": "192.168.1.100",
    "porta_servidor_tl1": "4567",
    "usuario_anm": "1",
    "senha_anm": "1",
    "ip_olt": "192.168.1.101",
    "fabricante": "FIBERHOME",
    "numero_pon": "12-02",
    "mac_onu": "FHTT09de3690",
    "tipo_onu": "FHTT01",
    "nome_cliente": "LUIZ GUILHERME SANTOS DE SOUZA",
    "vlan": "4000"
}
```

Sim, só isso! Metodo post para provisionar, desprovisionar, ler sinal. 

## OLT's suportados

Atualmente o OpenBoleto funciona com os bancos abaixo:

<table>
    <tr>
        <th>Fabricante</th>
        <th>Método</th>
        <th>Situação</th>
        </tr>
    <tr>
        <td>Fiberhome</td>
        <td>TL1</td>
        <td>Beta</td>
    </tr>
    <tr>
        <td>Huawei</td>
        <td>TL1</td>
        <td>Beta</td>
    </tr> 
    <tr>
        <td>Huawei</td>
        <td>telnet</td>
        <td>Beta</td>
    </tr>
 </table>


## Licença

- MIT License
