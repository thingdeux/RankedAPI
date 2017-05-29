#!/usr/bin/env bash
echo "export WORKON_HOME=$HOME/src/ranked-venv" >> /home/ec2-user/.bash_profile
echo "export PROJECT_HOME=$HOME/src/ranked/" >> /home/ec2-user/.bash_profile
echo "export VIRTUALENVWRAPPER_SCRIPT=/usr/local/bin/virtualenvwrapper.sh" >> /home/ec2-user/.bash_profile
echo "source /usr/local/bin/virtualenvwrapper_lazy.sh" >> /home/ec2-user/.bash_profile
