#!/bin/sh

FORCE_RUN=false
DEBUG=false

# When sourcing a script, OPTIND can be set to a value past the length of the options,
# this ensures it is set to the beginning.
OPTIND=1
while getopts ':fd' option; do
    case $option in
        f)
            FORCE_RUN=true
            ;;
        d)
            DEBUG=true
            ;;
        \?)
            echo "Invalid option. Only -f and -d are accepted."
            exit;;
    esac
done

SHELL_NAME=$(basename ${SHELL})
IS_BEING_SOURCED=false

if [ "${FORCE_RUN}" != true ]; then
    if [ "${SHELL_NAME}" = "bash" ] && [ "${BASH_SOURCE}" != "${0}" ]; then
        IS_BEING_SOURCED=true
    elif [ "${SHELL_NAME}" = "zsh" ] && [ "${ZSH_EVAL_CONTEXT}" = "toplevel:file" ]; then
        IS_BEING_SOURCED=true
    fi
fi

if [ "${DEBUG}" = "true" ]; then
    echo
    echo '~~~~~~~~~~~~~'
    echo 'debug info:'
    echo '~~~~~~~~~~~~~'
    echo force flag set = \"${FORCE_RUN}\"
    echo shell = \"${SHELL}\"
    echo shell name = \"${SHELL_NAME}\"
    echo '$0' = \"${0}\"
    echo bash source = \"${BASH_SOURCE}\"
    echo zsh eval context = \"${ZSH_EVAL_CONTEXT}\"
    echo is being sourced = \"${IS_BEING_SOURCED}\"
    echo '~~~~~~~~~~~~~'
    echo
fi

if [ "${FORCE_RUN}" = "false" ] && [ "${IS_BEING_SOURCED}" = "false" ]; then
    echo "ERROR: This script needs to be sourced to work as intended."
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

    if [ "$(expr substr $(uname -s) 1 5)" = "Linux" ]; then
      apt-get install python3-tk
    fi

    if [ -f requirements.txt ]; then
      pip install -r requirements.txt
    fi
fi
