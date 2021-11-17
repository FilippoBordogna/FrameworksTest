from flask import Flask, url_for, request, render_template
from markupsafe import escape

app = Flask(__name__) # Creo l'istanza della classe Flask

# ROUTE SEMPLICI

@app.route("/") # URL triggerata
def index(): # Funzione associata all'URL
    return "index"

@app.route('/login', methods=['GET', 'POST']) # Dichiaro che l'URL login può essere chiamata sia come GET che come POST
def login():
    if request.method == 'POST': # Chiamata POST
        #return do_the_login()
        return "Metodo POST"
    else: # Chiamata GET
        #return show_the_login_form()
        return "Metodo GET"

# ROUTE PARAMETRICHE

'''
COMMENTO PERCHE' CREA CONFLITTO
@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!" # Protezione da Injection mediante funzione escape
		 # f ci dice che ciò che è tra {...} è da ritenersi istruzione
'''

@app.route('/user/<username>')
def profile(username):
    return f'Profilo di {escape(username)}'

'''
TEST MOMENTANEAMENTE DISATTIVATI PER NON INCASINARE LA SHELL
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

with app.test_request_context('/hello', method='POST'):
    assert request.path == '/hello' # Se l'asserzione è falsa lancia errore altrimenti nulla
    assert request.method == 'POST'
'''

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name) # Ritorno la pagina HTML mediante template 'hello.html' a cui passo il parametro name