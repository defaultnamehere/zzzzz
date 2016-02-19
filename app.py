
from flask import Flask, render_template, send_file
import os

app = Flask('stalky')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("main.html")

@app.route('/data/<query>')
def get_data_for_query(query):
    for filename in os.listdir("generated_graphs/csv/"):
        if(query in filename):
            return send_file("generated_graphs/csv/{filename}".format(filename=filename))        
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
