import os, json, sys
from azureml.core import Workspace
from azureml.core import Run
from azureml.core import Experiment
from azureml.core.model import Model
import tensorflow as tf
from onnx_tf.frontend import tensorflow_graph_to_onnx_model
from azureml.core.runconfig import RunConfiguration
from azureml.core.authentication import AzureCliAuthentication
cli_auth = AzureCliAuthentication()

# Get workspace
ws = Workspace.from_config(auth=cli_auth)

# Get the latest evaluation result
try:
    with open("run_id.json") as f:
        config = json.load(f)
    if not config["run_id"]:
        raise Exception("No new model to register as production model perform better")
except:
    print("No new model to register as production model perform better")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)


with tf.gfile.GFile("frozen_graph.pb", "rb") as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    onnx_model = tensorflow_graph_to_onnx_model(graph_def,
                                     "fc2/add",
                                     opset=6)

    file = open("mnist.onnx", "wb")
    file.write(onnx_model.SerializeToString())
    file.close()

print(onnx_model.graph.node[0])

run_id = config["run_id"]
experiment_name = config["experiment_name"]
exp = Experiment(workspace=ws, name=experiment_name)

run = Run(experiment=exp, run_id=run_id)
names = run.get_file_names
names()
print("Run ID for last run: {}".format(run_id))
model_local_dir = "model"
os.makedirs(model_local_dir, exist_ok=True)

model = Model.register(model_path = "mnist.onnx",
                       model_name = "MNIST ONNX model",
                       tags = ["onnx"],
                       description = "test",
                       workspace = ws)

# Remove the evaluate.json as we no longer need it
# os.remove("aml_config/evaluate.json")

# Writing the registered model details to /aml_config/model.json
model_json = {}
model_json["model_name"] = model.name
model_json["model_version"] = model.version
model_json["run_id"] = run_id
with open("./outputs/model.json", "w") as outfile:
    json.dump(model_json, outfile)