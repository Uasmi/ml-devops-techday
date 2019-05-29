# ml-devops-techday
Machine Learning and DevOps Lab from workshop
Before start, clone this repository to prefered location

# Setup Azure Machine Learning Workspace:
To setup a workspace please run a Jupyter notebook called ```DevOps for ML.ipynb```
Then follow the instructions from IPython Notebook


# Azure DevOps
First you need to login to your DevOps envirenment. To do that go to <http://dev.azure.com>
![](https://githubpics.blob.core.windows.net/pictures/logindevops.jpg)

After that, press **+ Create Project** button:
![](https://githubpics.blob.core.windows.net/pictures/devopscreateproject.jpg)

Then jump to the **Repo** tab, choose **File**, then **Import** and Paste the link of this repository, or just upload a copy from your local PC
![](https://githubpics.blob.core.windows.net/pictures/devopsimportstep1.jpg)

# Setting up CI and CD
To setup CI and CD pipelines, we will use import functionality of Azure DevOps. There are two ways of importing pipelines: yaml and json.
Because we want to use classic visual editor, in this example we're going to import JSON templates.


To do that, jump to **Pipelines** tab, choose **Build** and press **New Pipeline**. You will need to jump to classic editor, select empty job and save it:
![](https://githubpics.blob.core.windows.net/pictures/pipelineEmptyJob.gif)

Then, go back to the **Build** tab and choose import button, navigate to your local repo copy and import JSON files from the **pipelines** folder.
Note: When the upload will finish, you will have to choose appropriate Azure Subscription from the drop-down list and press Authorize:
![](https://githubpics.blob.core.windows.net/pictures/pipelineImporting.gif)

For now, don't initialize the queue and choose **Save** in **Save & queue drop-down**

Now, repeat the same process for Release Pipeline:
![](https://githubpics.blob.core.windows.net/pictures/pipelineImportingRelease.gif)

We will also need to add two artifacts for that Release Pipeline: Build and Repo.
Setup the trigger at the Build pipeline and mark the Repo artifact as **Primary**:
![](https://githubpics.blob.core.windows.net/pictures/pipelineArtifacts.gif)
![](https://githubpics.blob.core.windows.net/pictures/primary.jpg)

# Queueing the pipelines
Before start the Build pipeline, make sure that the config.json contains all the required information.
You can alway grab config.json by jumping to **Azure Portal** and navigating to your **Machine Learning Workspace:**
![](https://githubpics.blob.core.windows.net/pictures/configJson.jpg)

Now feel free to go to **Build** tab, press **Queue** button and take a **coffee**.
This will trigger (the **Queue** button, not getting your **coffee**) the **Build Pipeline** where we:
1. Connect to Azure ML Services
2. Initialize training of neural network on full data
3. Validate results and compare with previous results (end exit if the results of new model is worse then the old one)
4. Freeze tensorflow graph 
5. Convert it to ONNX format
6. Register it to Azure ML Services

Succesfull build triggers the **Release Pipeline**, which does:
1. Creation of Docker container
2. Deployment to staging environment (ACI)

# Setting up CI
To setup a CI we need to add Branch Policy to Master. We set a requirement to finish the Build Pipeline.

# Understanding the scripts:
Detailed explanation of the scripts will be available later, however feel free to reverse engineer them right now. :)
