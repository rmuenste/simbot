# simbot
Project Setup
This guide explains how to set up a Python virtual environment for this project and install the required dependencies.

1. Create a Virtual Environment
To create a virtual environment named env, run the following command in your terminal:
python -m venv env
2. Activate the Virtual Environment
On Windows:
.\env\Scripts\activate
On macOS and Linux:
source env/bin/activate
You will know that the virtual environment is activated when (env) appears at the beginning of your terminal prompt.
3. Install Requirements
Once the virtual environment is activated, you can install the project dependencies specified in the requirements.txt file by running:
pip install -r requirements.txt
4. Deactivate the Virtual Environment
When you're done working, you can deactivate the virtual environment by simply running:
deactivate
This will return you to your global Python environment.

