from fsp import app   # import app from __init__ module
import os

"File .py necessary in order to run the Flas web application on localhost, the number port 9000 has been chosen arbitrarily"


if __name__ == '__main__':
    app.run(host='localhost',port=9000, debug=False)
    #os.system('lt --subdomain foodsharingpoint --port 9000') #http tunneling terminal additional command