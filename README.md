# Network-stats Flask app
Flask app to display network interface info.

## Get started
- Clone the repo
- Create python virtual environment  
    ```
    python3 -m venv venv
    ```
- Install the requirements
    ```
    pip install -r requirements.txt
    ```
- Start the virtual env  
    ```
    source ./venv/bin/activate  # for linux
    ./venv/Scripts/activate     # for Windows
    ```
- Create env variables for development
    ```
    # for bash:
    export FLASK_APP=app
    export FLASK_ENV=development

    # for powershell
    $env:FLASK_APP=app
    $env:FLASK_ENV=development
    ```
- Start the App
    ```
    flask run
    ```
