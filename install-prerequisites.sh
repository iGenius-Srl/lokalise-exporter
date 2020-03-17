#!/bin/bash -e

if [ "$(uname)" == "Darwin" ]; then

  echo "So, you are a macOS user! Fine, I'm going to install brew, python3, pip and igenius-lokalise-exporter"

  if ! type "brew" 2> /dev/null; then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  fi

  if ! type "python3" 2> /dev/null; then
    xcode-select --install
    brew install python3
  fi

  if ! type "pip" 2> /dev/null; then
    curl -L https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm -rf get-pip.py
  fi

  # Uninstall old lokalise-exporter 
  if pip3 show lokalise-exporter 2> /dev/null; then
    echo "> Uninstalling legacy lokalise-exporter lib"
    pip3 uninstall -y lokalise-exporter
  fi

  # Install igenius-lokalise-exporter
  if ! type "lokalise-exporter" 2> /dev/null; then
    echo "> Installing igenius-lokalise-exporter"
    pip3 install igenius-lokalise-exporter
  else
    echo "> Trying to upgrade igenius-lokalise-exporter"
    pip3 install igenius-lokalise-exporter --upgrade
  fi

else

  echo "So, you are on a linux or windows box. Let's use your current python installation!"

  if ! type "pip" 2> /dev/null; then
    curl -L https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    rm -rf get-pip.py
  fi

  if ! type "lokalise-exporter" 2> /dev/null; then
    pip install igenius-lokalise-exporter
  else
    pip install igenius-lokalise-exporter --upgrade
  fi

fi

echo "You're done! Now you can simply use lokalise-exporter from command line!"
