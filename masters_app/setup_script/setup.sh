#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

setup_virtualenv() {
  info 'Setting up virtualenv...'
  pip install virtualenv

  virtualenv '.env'
  source ".env/bin/activate"

  pip install -r requirement.txt
  finish 'Virtualenv setup finish.'

  # create superuser
  python manage.py createsuperuser
}

update_system() {
  info 'Installing system updates...'
  brew update
  finish 'System updates installed.'
}

info() {
  echo -e "${YELLOW}${1}${NC}"
}

finish() {
  echo -e "${GREEN}${1}${NC}"
}

update_system
setup_virtualenv
