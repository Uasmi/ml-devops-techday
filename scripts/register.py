from azureml.core.model import Model
from azureml.core import Workspace

ws = Workspace.from_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')

model = Model.register(model_path = "model/model.onnx",
                       model_name = "ONNX_MNIST_Model",
                       tags = {"type":"onnx"},
                       description = "test",
                       workspace = ws)