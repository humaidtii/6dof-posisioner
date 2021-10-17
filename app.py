from flask import Flask, render_template, request, redirect

from qualisys import QtmChecker

app = Flask(__name__,
        static_url_path='',
        static_folder='static')

labels = [ ]
qtm = None

@app.route('/', methods=["POST", "GET"])
def index():
    global qtm
    if request.args.get("body") in qtm.pos:
        # TODO load bookmark
        return render_template('pos.html')
    else:
        print(qtm.pos)
        return render_template('index.html', labels=qtm.pos.keys())

@app.route('/pull.json')
def pull():
    body = request.args.get("body")
    if body not in qtm.pos:
        return {"error": 1}
    pos = qtm.pos[body]
    x = float(request.args.get("x"))
    y = float(request.args.get("y"))
    z = float(request.args.get("z"))
    res = {
        "offset_x": round(x - pos[0], 2),
        "offset_y": round(y - pos[1], 2),
        "offset_z": round(z - pos[2], 2),
        "actual_x": pos[0],
        "actual_y": pos[1],
        "actual_z": pos[2],
    }
    print(res)
    return res

@app.route('/reload')
def reload():
    qtm.update_bodies()
    return redirect("/")

if __name__ == '__main__':
    qtm = QtmChecker()

    app.run(debug=True, host='0.0.0.0')
