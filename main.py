from flask import Flask
from getVersion import mariadb,mysql

app = Flask(__name__)

@app.route('/getversion')
def getVersion():
    dic=mysql.get_version()
    return dic

if __name__ == '__main__':
    app.run('0.0.0.0',8899)