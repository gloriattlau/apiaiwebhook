#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

from datetime import datetime
from datetime import date

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") != "intakeAction":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    name = parameters.get("name")
    res = makeWebhookResult(parameters)
    return res

def calculate_age(born):
    today = date.today()
    born = datetime.strptime(born, '%Y-%m-%d')
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def makeWebhookResult(parameters):
    print "HERE1"
    name = parameters.get("name")
    gender = parameters.get("gender")
    dob = parameters.get("dob")
    day = parameters.get("day")
    worsening = parameters.get("worsening")
    is_productive = parameters.get("is_productive")
    color = parameters.get("color")
    is_dyspnea = parameters.get("is_dyspnea")
    dyspnea_severity = parameters.get("dyspnea_severity")
    dyspnea_when = parameters.get("dyspnea_when")
    dyspnea_pain = parameters.get("dyspnea_pain")
    dyspnea_worsening = parameters.get("dyspnea_worsening")
    is_fever = parameters.get("is_fever")
    has_taken_temp = parameters.get("has_taken_temp")
    is_med = parameters.get("is_med")
            
    if parameters is None:
        return {}
    print "HERE2"
    
    if (gender == "F"):
        subject = "She"
    else:
        subject = "He"

    if (day == "1"):
        day = "1 day"
    else:
        day = day + " days"

    print "HERE3"
    condition = ""
    if (is_fever != "no"):
        condition = "subjective fever and "
    else:
        condition = "no subjective fever and "

    if (worsening == "worse"):
        condition = condition + "worsening cough"
    elif (worsening == "better"):
        condition = condition + "recovering cough"
    else:
        condition = condition + "cough that does not seem to be getting better or worse"

    productive = "not productive"
    if (is_productive == "yes"):
        productive = "productive of " + color + " sputum"
        
    dyspnea = "no dyspnea "
    if (is_dyspnea == "yes"):
        if (dyspnea_when == "when i cough"):
            dyspnea_when = "when " + subject.lower() + " coughs"
        dyspnea = dyspnea_severity + " dyspnea " + dyspnea_when + " "

    pleuritic_chest_pain = "has no pleuritic chest pain"
    if (dyspnea_pain == "yes"):
        pleuritic_chest_pain = "has pleuritic chest pain"

    med = "not taken any medications to treat this problem"
    if (is_med):
        med = is_med

    speech = name.title() + " is a " + str(calculate_age(dob)) + "yo " + gender + " who presents with " + day + " of " + condition + " that is " + productive + "." + subject + " reports " + dyspnea + "and " + pleuritic_chest_pain + ". " + subject + " has " + med + ". Nothing seems to make this problem better or worse."
        
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiaiwebhook"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
