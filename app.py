from flask import Flask, render_template, request

from qualisys import fetch_labels

app = Flask(__name__,
        static_url_path='',
        static_folder='static')
labels = [ ]
@app.route('/', methods=["POST", "GET"])
def index():
    if request.args.get("body") in labels:
        # TODO load bookmark
        return render_template('pos.html')
    else:
        return render_template('index.html', labels=labels)


if __name__ == '__main__':
    labels = fetch_labels()

    app.run(debug=True, host='0.0.0.0')
