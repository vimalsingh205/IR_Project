
from flask import Flask, render_template, request, json
from IRSearchEngine import searchEngine
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test')
def test():
    print('test')
    return render_template('index.html')

@app.route("/inputsearchvalue", methods=['GET'])
def inputsearchvalue():
    searchValue = request.args.get('searchKeyword');
    print(searchValue)
    result = searchEngine(searchValue)
    res = ", ".join(map(str, result))
    return res



if __name__ == '__main__':
    app.run(host='localhost', port=9874)
  