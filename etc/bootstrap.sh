#!/bin/bash

# Installation settings

PROJECT_NAME='regiohelden'

DB_NAME=$PROJECT_NAME
VIRTUALENV_NAME=$PROJECT_NAME

PROJECT_DIR=/home/vagrant/$PROJECT_NAME
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

echo '##########'
echo 'Updating the world'
echo '##########'
apt-get update -y

echo '##########'
echo 'Installing python and pip'
echo '##########'
apt-get install -y build-essential python python3-dev
curl -s https://bootstrap.pypa.io/get-pip.py | python3

echo '##########'
echo 'Installing postgresql'
echo '##########'
apt-get install -y postgresql libpq-dev
su - postgres -c "createuser -s vagrant"
su - vagrant -c "createdb $DB_NAME"

echo '##########'
echo 'Installing and configuring virtualenv and virtualenvwrapper'
echo '##########'
if [[ ! -f /usr/local/bin/virtualenv ]]; then
    pip3 install virtualenv virtualenvwrapper stevedore virtualenv-clone
fi

su - vagrant -c "/usr/local/bin/virtualenv $VIRTUALENV_DIR --python=/usr/bin/python3 && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    $VIRTUALENV_DIR/bin/pip install -r $PROJECT_DIR/requirements.txt"

cp -p ~vagrant/etc/bashrc ~vagrant/.bashrc

echo "# Virtualenv settings" >> ~vagrant/.bashrc
echo "export WORKON_HOME=~vagrant/.virtualenvs" >> ~vagrant/.bashrc
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~vagrant/.bashrc
echo "workon $VIRTUALENV_NAME" >> ~vagrant/.bashrc

chmod a+x $PROJECT_DIR/manage.py

su - vagrant -c "source $VIRTUALENV_DIR/bin/activate && cd $PROJECT_DIR && ./manage.py migrate"
su - vagrant -c "source $VIRTUALENV_DIR/bin/activate && cd $PROJECT_DIR && ./manage.py loaddata initial.json"
