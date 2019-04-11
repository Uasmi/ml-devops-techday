import os, json, sys
from azureml.core import Workspace
from azureml.core import Run
from azureml.core import Experiment
from azureml.core.model import Model
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

run_id = config["run_id"]
experiment_name = config["experiment_name"]
exp = Experiment(workspace=ws, name=experiment_name)

run = Run(experiment=exp, run_id=run_id)

os.makedirs('../mnist-tf/ckpt', exist_ok=True)

for f in run.get_file_names():
    if f.startswith('outputs/model'):
        output_file_path = os.path.join('../mnist-tf/ckpt/', f.split('/')[-1])
        print('Downloading from {} to {} ...'.format(f, output_file_path))
        run.download_file(name=f, output_file_path=output_file_path)