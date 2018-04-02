from flask import Flask

app = Flask(__name__)

#入口页面
@app.route('/')
def index():
    return 'Index Page'
#查询
@app.route('/search')
def search():
    return 'Hello, World'
#
if __name__ == '__main__':
    app.run()