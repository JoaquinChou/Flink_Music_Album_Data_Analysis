from flask import render_template
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<filename>')
def req_file(filename):
    return render_template(filename)


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = True
app.run()
