from azureml.core.model import Model
from azureml.core import Workspace
from azureml.core.image import ContainerImage
from azureml.core.conda_dependencies import CondaDependencies 
import os, json

ws = Workspace.from_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')
os.listdir()
print("Directories and files above")

os.chdir("./deployments")

model_name = "ONNX_MNIST_Model"


model = Model(name = model_name, workspace = ws)
model.download(target_dir='', exist_ok=False, exists_ok=None)

print ("Model ... ", model, model.name, model.description, model.version)

for entry in os.scandir('.'):
    if entry.is_file():
        print(entry.name)

myenv = CondaDependencies.create(pip_packages=["numpy","onnxruntime","azureml-core"])
with open("myenv.yml","w") as f:
    f.write(myenv.serialize_to_string())

os.listdir()
print("Directories and files above")


image_config = ContainerImage.image_configuration(execution_script = "score.py",
                                                  runtime = "python",
                                                  conda_file = "myenv.yml",
                                                  description = "test",
                                                  tags = {"tag":"onnx"}
                                                 )

image = ContainerImage.create(name = "myonnxmodelimage",
                              # this is the model object
                              models = [model],
                              image_config = image_config,
                              workspace = ws)

image.wait_for_creation(show_output = True)

if image.creation_state != "Succeeded":
    raise Exception("Image creation status: {image.creation_state}")

print(
    "{}(v.{} [{}]) stored at {} with build log {}".format(
        image.name,
        image.version,
        image.creation_state,
        image.image_location,
        image.image_build_log_uri,
    )
)

# Writing the image details to /aml_config/image.json
image_json = {}
image_json["image_name"] = image.name
image_json["image_version"] = image.version
image_json["image_location"] = image.image_location
with open("./image.json", "w") as outfile:
    json.dump(image_json, outfile)