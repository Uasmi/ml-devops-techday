import numpy
import os, json, datetime, sys
from operator import attrgetter
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice import AciWebservice
from azureml.core.authentication import AzureCliAuthentication
import cv2
import matplotlib.image as mpimg

cli_auth = AzureCliAuthentication()
# Get workspace
ws = Workspace.from_config(auth=cli_auth)
# Get the ACI Details
try:
    with open("aml_config/aci_webservice.json") as f:
        config = json.load(f)
except:
    print("No new model, thus no deployment on ACI")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)

service_name = config["aci_name"]
# Get the hosted web service
service = Webservice(name=service_name, workspace=ws)

# Input for Model with all features



img = mpimg.imread(your_test_image)
img = preprocess(img)

input_data = json.dumps({'data': img.tolist()})
your_test_image = "<path to file>"

    try:
        r = aci_service.run(input_data)
        result = r['result']
        time_ms = np.round(r['time_in_sec'] * 1000, 2)
        print (result, time_ms)
    except KeyError as e:
        raise Exception("ACI service is not working as expected")
