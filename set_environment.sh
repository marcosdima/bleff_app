#!/bin/bash

# Virtual environment directory name
venv_dir=myenv

# Create virtual environment
python3 -m venv $venv_dir

# Activate the virtual environment
source $venv_dir/bin/activate

# Install packages
pip install flask
pip install Flask-SQLAlchemy
pip install flask-marshmallow
pip install marshmallow-sqlalchemy

# Deactivate the virtual environment
deactivate

echo "Installation completed. Virtual environment created and packages installed."
