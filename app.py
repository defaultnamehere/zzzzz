
from flask import Flask, render_template, send_file


app = Flask('stalky')

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/data/<int:uid>')
def get_data_for_uid(uid):
    return send_file("generated_graphs/csv/{uid}.csv".format(uid=uid))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
