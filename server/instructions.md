# Diep-Clone Backend

This diep.io clone uses Python with FastApi for backend.

## Installation
----

> [!IMPORTANT]
> If working in main directory (contains client and server directories), you must first enter the server directory before
> running any commands via `cd server`

### Installation with VENV

To setup your venv and package installation, press `CTRL + SHFT + P`, and select `Python: Select Interpreter`.
You can select either `Quick Create` or `venv` for python to create the virtual environment in the project.

After setting up the venv, you should have a `.venv` file in `server` directory.
To activate the virtual env run  (Windows) `.venv/Scripts/activate` or (Linux / macOS) `source venv/bin/activate`

> [!IMPORTANT]
> If you didn't use `Python: Select Interpreter` to create the venv, run
> ```sh
> # For linux / macOS
> python3 -m venv venv
>
> # For Windows
> python -m venv .venv
> ```
>
> You must set the python interpreter for this environment to point to `.venv/Scripts/python.exe`
> To do this, press `CTRL + SHFT + P`, and select `Python: Select Interpreter`.

To install required packages, run `pip install -r requirements.txt` or `python -m pip install -r requirements.txt`

### Installation without a VENV

Just install required packages, run `pip install -r requirements.txt`
