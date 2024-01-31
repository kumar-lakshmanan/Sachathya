#For Sachathya
import os
import sip
from http.server import HTTPServer
import HTTPAppServerLogic as coreLogicServer

import importlib 
importlib.reload(coreLogicServer)
		
if (__name__=="__main__"):
	HOST, PORT = '127.0.0.1', 8082
	print("Started HTTP Server")
	print("Try the url...")
	print("http://%s:%s/add/121/434'"%(HOST,PORT))		
	server = HTTPServer((HOST, PORT), coreLogicServer.httpRequestHandler)
	server.serve_forever()
