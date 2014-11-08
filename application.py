from flask import Flask, render_template
from eve import Eve
from os.path import abspath, dirname

app = Eve()
app.root_path = abspath(dirname(__file__))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
	app.debug = True
	app.run()
