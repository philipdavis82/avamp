#!/bin/bash
# # Absolute path to this script, e.g. /home/user/bin/foo.sh
# SCRIPT=$(readlink -f "$0")
# # Absolute path this script is in, thus /home/user/bin
# BASEDIR=$(dirname "$SCRIPT")

# cd $BASEDIR/..
echo "Activating pyenv 3.11"

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

pyenv shell 3.11.14
echo "Activating local enviroment"
source ./env/bin/activate

echo "Done"