# Sistema contable "accountingbook"


## Requisitos previos:
Son herramientas que debes tener instaladas en tu máquina local.

1. **Python 3.11** -- https://www.python.org/downloads/
2. **pip** -- https://pip.pypa.io/en/stable/installation/
2. **Virtualenv** -- https://pypi.org/project/virtualenv/
2. **Virtualenvwrapper-win** -- https://pypi.org/project/virtualenvwrapper-win/

## Creación de ambiente para desarrollo
1. Crear en ambiente con el comando: `` virtualenv <nombre del ambiente> ``.  
si tu variable de entorno de python es **py** debes ejecutar el comando: `` virtualenv -p py <nombre del ambiente> ``, esto tomará tu python global y la version 3.11  
2. Entrar al ambiente: `` workon <nombre del ambiente> ``.
3. Instalación de dependencias: `` pip install -r requirements.txt ``.

## Correr migraciones
1. Correr migraciones: `` python manage.py migrate `` o `` py manage.py migrate `` si tu  
varible de entorno es **py**

## Correrr servidor
1. Ejecutar: `` python manage.py runserver`` o `` py manage.py runserver ``
2. Ve a la url: **http://127.0.0.1:8000/** de tu navegador

## Crear super usuario para el admin
1. ejecutar el comando: `` python manage.py createsuperuser `` o `` py manage.py createsuperuser ``
2. Ingresa el nombre del usuario, correo y password.
3. Ve a la url **http://127.0.0.1:8000/admin** y has login

Listo. :)