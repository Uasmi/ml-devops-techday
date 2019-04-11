import os, json, datetime, sys
from operator import attrgetter
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice import AciWebservice
from azureml.core.authentication import AzureCliAuthentication

cli_auth = AzureCliAuthentication()
# Get workspace
ws = Workspace.from_config(auth=cli_auth)# Get the Image to deploy details


image = Image(workspace = ws, name="myonnxmodelimage")
print (image)

aciconfig = AciWebservice.deploy_configuration(
    cpu_cores=1,
    memory_gb=1,
    tags={"area": "MNIST", "type": "DNN"},
    description="Description",
)

aci_service_name = "aciwebservice"

service = Webservice.deploy_from_image(
    deployment_config=aciconfig, image=image, name=aci_service_name, workspace=ws
)

service.wait_for_deployment()
print(
    "Deployed ACI Webservice: {} \nWebservice Uri: {}".format(
        service.name, service.scoring_uri
    )
)

# service=Webservice(name ='aciws0622', workspace =ws)
# Writing the ACI details to /aml_config/aci_webservice.json
aci_webservice = {}
aci_webservice["aci_name"] = service.name
aci_webservice["aci_url"] = service.scoring_uri
with open("./aci_webservice.json", "w") as outfile:
    json.dump(aci_webservice, outfile)