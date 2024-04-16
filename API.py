from flask import Flask, request, redirect, jsonify, Response
import random, requests, re, json

app = Flask("Ephoto360-Random-Image-Generator-For-Github")

client = False

def createSession():
    global client
    session = requests.Session()
    url = "https://en.ephoto360.com/create-glossy-silver-3d-text-effect-online-802.html"
    req = session.get(url)
    data = {
        "autocomplete0": "",
        "text": ["Gusti"],
        "submit": "GO",
        "token": re.search("name=\"token\" value=\"(.*?)\"", req.text).group(1),
        "build_server": re.search("name=\"build_server\" value=\"(.*?)\"", req.text).group(1),
        "build_server_id": re.search("name=\"build_server_id\" value=\"(.*?)\"", req.text).group(1),
    }
    res = session.post(url, data=data)
    payload = json.loads(re.search("name=\"form_value_input\" value=\"(.*?)\"", res.text).group(1).replace("&quot;", "\""))
    del payload["text"]
    client = {
        "session": session,
        "payload": payload
    }

class EphotoModel:
    def __init__(self, text, client):
        self.text = text
        self.ids = [
            "809",
            "797",
            "767",
            "589",
            "811",
            "808",
            "769",
            "768",
            "717",
            "706",
            "682",
            "673",
            "668",
            "658",
            "655",
            "619",
            "595",
            "594",
            "576",
            "521",
            "469",
            "441",
            "424",
            "153",
            "108",
            "85",
            "74",
            "59",
            "17",
            "807",
            "798",
            "704",
            "698",
            "695",
            "686",
            "685",
            "683",
            "618",
            "597",
            "582",
            "580",
            "577",
            "506",
            "397",
            "376",
            "372",
            "369",
            "359",
            "357",
            "356",
            "347",
            "343",
            "342",
            "341",
            "340",
            "329",
            "288",
            "285",
            "278",
            "248",
            "215",
            "210",
            "206",
            "204",
            "200",
            "199",
            "194",
            "188",
            "187",
            "184",
            "156",
            "147",
            "143",
            "139",
            "126",
            "111",
            "110",
            "109",
            "97",
            "88",
            "86",
            "84",
            "75",
            "73",
            "72",
            "69",
            "68",
            "63",
            "61",
            "30",
        ]
        self.client = client

    def randomId(self):
        return random.choice(self.ids)

    def getImage(self):
        if not self.client:
            return False
        self.client.get("payload")["text[]"] = [self.text]
        self.client.get("payload")["id"] = self.randomId()
        resp = self.client.get("session").post("https://en.ephoto360.com/effect/create-image", data=self.client.get("payload")).json()
        return self.getRaw(self.client.get("payload")["build_server"] + resp.get("image"))

    def getRaw(self, urlImage):
        rawImage = self.client.get("session").get(urlImage, stream=True).raw
        return rawImage

class EphotoView:
    def renderview(self, response):
        rawResponse = response.getImage()
        if not rawResponse:
            return False
        return Response(rawResponse, mimetype="image/jpg")

class EphotoController:
    def __init__(self, ephotomodel, ephotoview):
       self.ephotomodel = ephotomodel
       self.ephotoview = ephotoview

    def response(self):
        return self.ephotoview.renderview(self.ephotomodel)

@app.route("/gusti", methods=["GET"])
def routehandler():
    teks = request.args.get("text")
    if not teks:
        return jsonify({"Error": "harus menyertakan parameter text"})
    model = EphotoModel(teks, client)
    view = EphotoView()
    controller = EphotoController(model, view)
    retview = controller.response()
    return retview if retview else jsonify({"error": "server sibuk"})

@app.route("/cronjob", methods=["GET"])
def cronjobTask():
    createSession()
    return jsonify({"error": "cron job"})

@app.route("/<apapun>", methods=["GET"])
def redirectKeGithub(apapun):
    return jsonify({"error": f"path /{apapun} tidak ada"})

@app.route("/", methods=["GET"])
def index():
    return redirect("https://github.com/GustiMuhammadKhotami/GitCoolName")
