from flask import render_template
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    # 使用render_template的方法来渲染页面
    return render_template('index.html')


@app.route('/<filename>')
def req_file(filename):
    return render_template(filename)


if __name__ == "__main__":
    # 代码调试生效
    app.debug = True
    # 模板调试立即生效
    app.jinja_env.auto_reload = True
app.run()
