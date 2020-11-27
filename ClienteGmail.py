import imaplib
import pprint
import re 
from getpass import getpass

 # Abre el archivo con los datos necesarios para el analisis #
with open('Datos.txt') as d:
    datos = d.read().splitlines()
    FROM = datos[0]
    EXPREG = datos[1]
    FECHA = datos[2] 
    print("Los datos a buscar son:")
    print("REMITENTE: "+FROM+'\n'+'EXPRESION REGULAR: '+EXPREG+'\n'+'Fecha mas antigua de la Exp. Regular: '+FECHA+'\n')

# Inicia sesion como cliente de correo electronico #
imap_host = 'imap.gmail.com' 
imap_user = str(raw_input('Ingrese su email:'))
imap_pass = getpass('Ingrese su Password:')
imap = imaplib.IMAP4_SSL(imap_host)
imap.login(imap_user, imap_pass)
imap.select('Inbox')
tmp, data = imap.search(None,'(FROM "'+FROM+'")')

# Funcion que analiza los Message-ID #
for itera in data[0].split(): 
        tmp, data = imap.fetch(itera, '(BODY[HEADER.FIELDS (FROM MESSAGE-ID DATE)])')
        print('Numero de mensaje en la bandeja de entrada:{0}'.format(itera))
        aux = str(data[0][1]).replace('\r\n', '\n')
        print('Los datos del correo son los siguientes:\n'+aux)
        mail = re.compile(r""""""+EXPREG+"""""", re.X)
        mails =  data[0][1].encode('utf-8')
        if re.search(mail, mails):
            x = mail.findall(mails)
            print('Analizando el Message-ID: '+str(x)+' se confirma que es un emisor real\n')
        else:
            print('ALERTA, POSIBLE PHISHING! al analizar el Message-ID, segun nuestros registros no presenta coincidencias.\n')
imap.close()