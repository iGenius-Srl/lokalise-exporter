#!/bin/bash -e

if [ "$(uname)" == "Darwin" ]; then

  echo "So, you are a macOS user! Fine, I'm going to install brew, python3, pip and lokalise-exporter"

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

  if ! type "lokalise-exporter" 2> /dev/null; then
    pip3 install lokalise-exporter
  else
    pip3 install lokalise-exporter --upgrade
  fi

else

  echo "So, you are on a linux or windows box. Let's use your current python installation!"

  if ! type "pip" 2> /dev/null; then
    curl -L https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    rm -rf get-pip.py
  fi

  if ! type "lokalise-exporter" 2> /dev/null; then
    pip install lokalise-exporter
  else
    pip install lokalise-exporter --upgrade
  fi

fi

echo "You're done! Now you can simply use lokalise-exporter from command line!"
