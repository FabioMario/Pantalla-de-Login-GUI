import PySimpleGUI as sg
import sqlite3
from authentication import *

def login():
    sg.theme('SandyBeach')
    layout = [
        [sg.Text('Ingrese su nombre de usuario y contraseña', justification='center', font=("Helvetica", 25))],
        [sg.Text('Usuario', size=(15, 1)), sg.InputText()],
        [sg.Text('Contraseña', size=(15, 1)), sg.InputText(password_char='*')],
        [sg.Submit('Ingresar', disabled=True, button_color=('black', 'green')),
         sg.Cancel('Cancelar'),
         sg.Cancel('Crear cuenta', button_color=('black', 'green'))]]
    window = sg.Window('Login', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        elif event == 'Crear cuenta':
            create_account2()
        elif event == 'Ingresar' and (values[0] != '' and values[1] != ''):
            window['Ingresar'].update(disabled=False)
            conn = sqlite3.connect('users1.db')
            c = conn.cursor()
            params = [values[0]]
            c.execute("SELECT password FROM users1 WHERE username = ?", params)
            data = c.fetchone()
            hashed_password = data[0]
            c.close()
            conn.close()
            if verify_password(values[1], hashed_password):
                sg.popup('Bienvenido')
                break
            else:
                sg.popup('Usuario o contraseña incorrectos')

        window['Ingresar'].update(disabled=True)
    window.close()

def create_account2():
    layout = [
        [sg.Text('Ingrese su nombre de usuario y contraseña', justification='center', font=("Helvetica", 25))],
        [sg.Text('Usuario', size=(15, 1)), sg.InputText(do_not_clear=False)],
        [sg.Text('Contraseña', size=(15, 1)), sg.InputText(password_char='*',do_not_clear=False)],
        [sg.Submit('Registrarse', button_color=('black', 'green')), sg.Cancel('Cancelar')]]
    window = sg.Window('Crear cuenta', layout)
    conn = sqlite3.connect('users1.db')
    c = conn.cursor()
    while True:
        event, values = window.read()
        if event == 'Registrarse' and (values[0] != '' and values[1] != ''):
            salty_hash = hash_password(values[1])
            try:
                c.execute('''CREATE TABLE IF NOT EXISTS users1(username text PRIMARY KEY, password bytea)''')
                c.execute("INSERT INTO users1 VALUES (?, ?)", (values[0], salty_hash))
                conn.commit()
                print("Usuario creado")
                sg.popup('Usuario creado')
                break
            except:
                sg.popup('Usuario ya existe')
        elif event == 'Cancelar' or event == sg.WIN_CLOSED:
            break
        elif event == 'Registrarse' and (values[0] == '' or values[1] == ''):
            sg.popup('Debe completar todos los campos')
    conn.close()
    window.close()
login()