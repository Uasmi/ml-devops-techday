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

Then jump to the **Repo** tab, choose **File**, then **Import** and Paste the link of this repository
![](https://githubpics.blob.core.windows.net/pictures/devopsimportstep1.jpg)

# Setting up CI and CD
To setup CI and CD pipelines, we will use import functionality of Azure DevOps. There are two ways of importing pipelines: yaml and json.
Because we want to use classic visual editor, in this example we're going to import JSON templates.
