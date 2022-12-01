import random
import string
import flask
import json
import hashlib

app = flask.Flask(__name__)

currAccNum = 0

systemKey = "dslhB W(WE&Y B(Py3qIJ OSUDaylsdah;liwudb p9eAURF"


def readData():
    with open(r"data.json", "r") as data:
        return json.loads(data.read())


def writeData(cont: dict):
    with open(r"data.json", "w") as data:
        data.write(json.dumps(cont))


@app.route("/leaderBoard", methods=["POST"])
def retLeaderBoard():
    x = readData()
    s = []
    for i in x:
        s.append([x[i]["score"], {"score": x[i]["score"], "crown": x[i]["crown"], "name": x[i]["name"]}])

    s.sort(key=firstElement)
    return json.dumps([i[1] for i in s])


@app.route("/updateData", methods=["POST"])
def updateData():
    global systemKey
    dat = flask.request.form.to_dict()
    x = readData()
    accNum = dat["accNum"]
    try:
        if not systemKey == dat["systemKey"]:
            return "wrong system key"

        if x[accNum]["online"]:
            if dat["key"] == x[accNum]["key"]:
                for i in dat:
                    if i != "key" and i != "accNum" and i != "systemKey":
                        try:
                            x[accNum][i] = dat[i]
                        except Exception as e:
                            return "Wrong params"
            else:
                return "wrong key. bad boi tryna hack"
        else:
            return "Bruh ur not even signed in"
    except Exception as e:
       print(e)
       return ":)"


def firstElement(e):
    return e[0]


@app.route("/getData", methods=["POST"])
def getData():
    dat = flask.request.form.to_dict()
    accNum = dat["accNum"]
    x = readData()
    try:
        if x[accNum]["online"]:
            if dat["key"] == x[accNum]["key"]:
                return x[accNum]
            else:
                return "wrong key. bad boi tryna hack"
        else:
            return "Bruh ur not even signed in"
    except Exception as e:
       print(e)
       return ":)"


@app.route("/signUp", methods=["POST"])
def signUp():
    global currAccNum
    dat = flask.request.form.to_dict()
    print(dat)
    try:
        dat["username"]
        dat["password"]
        dat["dob"]
        dat["email"]
    except KeyError:
        return "Invalid request"

    new = readData()
    key = ''.join(random.choices(string.ascii_letters + string.digits + string.digits, k=10))
    new[str(currAccNum)] = {"username": dat["username"], "password": hashlib.sha256(dat["password"].encode()).hexdigest(),
                            "dob": dat["dob"], "coins": 0, "crown": "iron", "itemsOwned": [],
                            "online": True, "key": key, "email": dat["email"]}

    writeData(new)
    currAccNum += 1
    return '{"status": "AccCreated", "key": "' + key + '", "accNumber":"' + f'{currAccNum}' '"}'


@app.route("/login", methods=["POST"])
def login():
    dat = flask.request.form.to_dict()
    x = readData()
    if dat["accNum"] in x.keys():

        if not x[dat["accNum"]]["online"] and hashlib.sha256(dat["password"].encode()).hexdigest() == x[dat["accNum"]]["password"]:
            x[dat["accNum"]]["online"] = True
            key = ''.join(random.choices(string.ascii_letters + string.digits + string.digits, k=10))
            x[dat["accNum"]]["key"] = key
            writeData(x)
            return '{"status": "AccLoggedIn", "key": "' + key + '"}'
        else:
            "that guys already online or u noob couldnt get the password right"
    else:
        "Account doesnt exist"


app.run()
