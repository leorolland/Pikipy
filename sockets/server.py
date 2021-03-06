# -*- Coding:Utf-8 -*-
import threading
import socketserver
 
from datetime import datetime
 
 
# Python vient avec ses serveurs socket tout prêts.
# Tout ce qu'il y a faire c'est créer une classe 
# de handler, c'est à dire l'objet qui va s'occuper
# des messages quand ils arrivent. On hérite du 
# handler de la lib standard, et on redéfinit juste
# handle() qui est la méthode qui va être appelée
# à chaque message.
class RequestHandler(socketserver.BaseRequestHandler):
 
    def handle(self):
        # on récupère des requêtes, et on répond avec
        # exactement le même message + un timestamp
        data = self.request.recv(1024)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        response = "reponse"
        self.request.sendall(bytes(response.encode('utf-8')))
 
# Pour le serveur, pas grand chose à faire à part le définir
# Ici je fais un serveur threadé pour le Lulz car ça
# ne sert pas à grand chose pour un client avec 3 messages
# synchrones
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
 
 
 
if __name__ == "__main__":
 
    # on instancie notre server et on lui passe le gestionnaire de
    # requêtes
    server = ThreadedTCPServer(('127.0.0.1', 6666), RequestHandler)
    ip, port = server.server_address
 
    # on start le thread pour le serveur et on le daemonise
    server_thread = threading.Thread(target=server.serve_forever)
 
    server_thread.daemon = True
    server_thread.start()
 
    # si on appuie sur "enter", raw_input() s'arrête et le serveur
    # est stoppé
    input("Hit enter to stop the server")
 
    server.shutdown()