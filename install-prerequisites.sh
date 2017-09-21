#!/bin/bash -e
API_KEY="cf00acf8128c8a24c38fcc659ccef228a06cc1ed"

MOBILE_V4="6604856959bf84410c9624.80778254"
ERRORS="61753052588efed4d4d222.49119459"
NOTIFIER="38518908595518996ec668.96620309"

PROJECTS="${MOBILE_V4}, ${ERRORS}, ${NOTIFIER}"

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
  fi

fi

echo "You're done! Now you can simply use lokalise-exporter from command line!"
