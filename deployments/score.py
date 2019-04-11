import onnxruntime
import json
import numpy as np
import sys
from azureml.core.model import Model

def init():
    global session
    model = Model.get_model_path(model_name = 'ONNX_MNIST_Model')
    session = onnxruntime.InferenceSession(model)

def preprocess(input_data_json):
    # convert the JSON data into the tensor input
    return np.array(json.loads(input_data_json)['data']).astype('float32')

def postprocess(result):
    return np.array(result).tolist()

def run(input_data_json):
    try:
        start = time.time()   # start timer
        input_data = preprocess(input_data_json)
        input_name = session.get_inputs()[0].name  # get the id of the first input of the model   
        result = session.run([], {input_name: input_data})
        end = time.time()     # stop timer
        return {"result": postprocess(result),
                "time": end - start}
    except Exception as e:
        result = str(e)
        return {"error": result}