#For Sachathya
from flask import Flask
from flask import request
import HTTPFlaskServerLogic as fs

app = Flask(__name__)        
if (__name__=="__main__"):
    HOST, PORT = 'localhost', 5000
    print("Started Flask Server")
    print("Try the url...")
    print("http://%s:%s'"%(HOST,PORT))
    fs.app.run(port=PORT)