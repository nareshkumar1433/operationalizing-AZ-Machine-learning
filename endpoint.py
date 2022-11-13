import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data =  {
  "Inputs": {
    "data": [
      {
        "age": 23,
        "job": "bank",
        "marital": "married",
        "education": "high school",
        "default": "yes",
        "housing": "yes",
        "contact": "ecellular",
        "month": "may",
        "day_of_week": "monday",
        "duration": 12,
        "campaign": 10,
        "pdays": 12,
        "previous": 10,
        "poutcome": "yes",
        "emp.var.rate": 10,
        "cons.price.idx": 2000,
        "cons.conf.idx": 2000,
        "euribor3m": 3.0,
        "nr.employed": 10000,
        "y": "y"
      }
    ]
  },
  "GlobalParameters": {
    "method": "predict"
  }
}

body = str.encode(json.dumps(data))

url = 'https://bankproj.southcentralus.inference.ml.azure.com/score'
api_key = 'SF2NpzwJDImgjMJdtGIwBOB6uno6bao8' # Replace this with the API key for the web service

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'bankproj' }

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))