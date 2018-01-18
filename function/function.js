const xhr = require("xhr");
const pubnub = require('pubnub');
const db = require("kvstore");
const api_key = 'AZURE_ML_KEY';

const body = {
    'Inputs': {
        'input1': [{
            'Rotation': request.message.rotation,
            "Temperature": request.message.temperature,
            "Vibration": request.message.vibration,
            "Sound": request.message.sound
        }]
    }
};

//Replace Azure_ML_Endpoint with actual endpoint
const url = "<AZURE_ML_ENDPOINT>";
var anomaly_count;

const http_options = {
    "method": "POST",
    "headers": {
        "Content-Type": "application/json",
        'Authorization': ('Bearer ' + api_key)
    },
    "body": body
};

db.get("anomaly_count").then((value) => {
    anomaly_count = value.count;
    if (anomaly_count == "undefined" || anomaly_count == "null") {
        anomaly_count = 0;
        db.set("anomaly_count", {
            'count': anomaly_count
        });
    }
});

return xhr.fetch(url, http_options).then((x) => {
    const body = JSON.parse(x.body);
    const anomaly_score = body.Results.output1[0]["Scored Probabilities"];
    var msg;
    if (anomaly_score > 0.7) {
        console.log("{'anomaly': true, 'score':" + anomaly_score + ", anomaly_count:" + anomaly_count + "}");
        if (anomaly_count >= 5) {
            msg = {
                'alarm': 'on'
            };
            anomaly_count = 0;
        }
        anomaly_count = anomaly_count + 1;
        db.set("anomaly_count", {
            'count': anomaly_count
        });
    } else {
        msg = {
            'alarm': 'off'
        };
    }
    pubnub.publish({
        "channel": "turbine.alarm",
        "message": msg
    }).then((publishResponse) => {});
    return request.ok();
});
