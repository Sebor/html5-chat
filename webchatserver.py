#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#----------------------------------------------------------------------------
# Name:         main.py
# Author:       JuanCarlosPaco  ( Argentina )
# Contact:      juancarlospaco@ubuntu.com , @juancarlospaco at Identi.Ca/Twitter
# License:      GPL v3
#----------------------------------------------------------------------------
# Dependencies: apt-get install python python-bottle
###############################################################################
try:
    import psyco  # Speed Up if avaliable
    psyco.full()
except ImportError:
    print(" No PYTHON-PSYCO avaliable... ")

###############################################################################

try: # Bottle imports
    import commands
    import os
    import sys
    import bottle
    from bottle import route
    from bottle import template
    from bottle import request
    from bottle import redirect
    from bottle import error
    from bottle import debug
    from bottle import run
except ImportError:
    print (' \n ERROR, IMPORT FAILED: \
    from framework.bottle import route, template, request, error, debug')

###############################################################################

# Indez
@bottle.route('/')
def index():
    output = template('client/client.html')
    return output

# Indez
@bottle.route('/oneline')
def oneline():
    output = template('client/onelineclient.html')
    return output

###############################################################################

# echo de IP for testings

@bottle.route('/my_ip')
def show_ip():
    ip = request.environ.get('REMOTE_ADDR')
    return " Tu IP es: %s" % ip

###############################################################################

# Manejo de Errores

# que hacer cuando la URL es invalida
@bottle.error(403) 
def mistake403(code):
    return '<!DOCTYPE html> <html> <head> \
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/> \
    <meta http-equiv="X-UA-Compatible" content="chrome=1"> \
    <link rel="shortcut icon" \
    href="http://www.ubuntu.com/sites/all/themes/ubuntu10/favicon.ico" \
    type="image/x-icon"/><META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW"> \
    <title>HTML5 Chat</title> </head> \
    <body style="color: rgb(0, 0, 0); background-color: rgb(51, 51, 51);"> \
    <center> <h1 style="text-align: center; color: white;"> ☠ <br> \
    ✗ ERROR: Disculpe, la URL es invalida, verifique la direccion.</h1> \
    </center> </body> </html>'

# que hacer cuando la pagina no existe
@bottle.error(404) 
def mistake404(code):
    return '<!DOCTYPE html> <html> <head> \
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/> \
    <meta http-equiv="X-UA-Compatible" content="chrome=1"> \
    <link rel="shortcut icon" \
    href="http://www.ubuntu.com/sites/all/themes/ubuntu10/favicon.ico" \
    type="image/x-icon"/><META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW"> \
    <title>HTML5 Chat</title> </head> \
    <body style="color: rgb(0, 0, 0); background-color: rgb(51, 51, 51);"> \
    <center> <h1 style="text-align: center; color: white;"> ☠ <br> \
    ✗ ERROR: Disculpe, la URL es inexistente, verifique la direccion.</h1> \
    </center> </body> </html>'

# Redireccion de URL por URL incorrecta
@bottle.route('/index.php') # YAY PHP puajjj!
def wrong():
    redirect("/")

###############################################################################

# Ejecucion de Main

def main():
    bottle.debug(True)# True para desarrollo, False para Produccion
    app = bottle.default_app()
    app.catchall = False # Mostrar excepciones mientras desarrollamos

    if sys.hexversion > 0x02050000: # Python version check
        pass # python version >= 2.5.0, do nothing
    else:    
        print "\n ERROR: Python version < 2.5.0\n" # python version under 2.5.0 dont work
        sys.exit(" ERROR: python version under 2.5.0 dont work...\n")
    
    os.system('/usr/bin/env `pwd`/server/chatserver.py &')#esto es una Cochinadaaaaaaaaaaaaaaa

    if os.geteuid()==0: # root check
        # True para desarrollo, False para Produccion
        bottle.run(app=app, host='0.0.0.0', port=80, reloader=True) # root=puerto 80,worldwide
    else:
        #logz = open('bottlelog.log', 'w') # write a LOG file BETA
        #sys.stdout = logz
        # True para desarrollo, False para Produccion
        bottle.run(app=app, host='127.0.0.1', port=8000, reloader=True) # non-root=puerto 8000,LAN
        #logz.close() 

###############################################################################

if __name__=="__main__":
    main()

###############################################################################
