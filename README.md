# simbot
Project Setup
This guide explains how to set up a Python virtual environment for this project and install the required dependencies.

1. Create a Virtual Environment
To create a virtual environment named env, run the following command in your terminal:
```
python -m venv env
```
3. Activate the Virtual Environment
On Windows:
```
.\env\Scripts\activate
```
On macOS and Linux:
```
source env/bin/activate
```
You will know that the virtual environment is activated when (env) appears at the beginning of your terminal prompt.
5. Install Requirements
Once the virtual environment is activated, you can install the project dependencies specified in the requirements.txt file by running:
```
pip install -r requirements.txt
```
6. Deactivate the Virtual Environment
When you're done working, you can deactivate the virtual environment by simply running:
```
deactivate
```
This will return you to your global Python environment.

7. Start the App
```
python3 ./sim_bot.py
```
The start command starts a chat interface that can be open in the browser using the url http://127.0.0.1:7860/ or similar. A dark theme can be
used by navigating to http://127.0.0.1:7860/?__theme=dark
