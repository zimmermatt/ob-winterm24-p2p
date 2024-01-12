#!/bin/sh

# Is this actually shell portable?
if [[ "${0}" =~ .*\.sh ]]; then
    echo "ERROR: This script needs to be sourced to work as intended."
    echo "Script name: ${0}"
    exit 42
else
    command -v pip3 > /dev/null 2>&1 || {
        echo "pip3 is not available - please install python3"
        return 1
    }

    command -v virtualenv > /dev/null 2>&1 || {
        pip3 install virtualenv
    }

    virtualenv --python=python3 venv

    if [ "$(uname)" = "Darwin" ] || [ "$(expr substr $(uname -s) 1 5)" = "Linux" ]; then
        source venv/bin/activate
    else
        source venv/Scripts/activate
    fi

    if [ -f requirements.txt ]; then
      pip install -r requirements.txt
    fi
fi

