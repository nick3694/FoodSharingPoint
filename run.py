from fsp import app   # import app automaticamente dal modulo __init__
import os

if __name__ == '__main__':
    app.run(host='localhost',port=5000, debug=False) #in order to reach the external links
    #os.system('lt --subdomain foodsharingpoint --port 5000')