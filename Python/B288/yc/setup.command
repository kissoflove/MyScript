#! /bin/bash
which -s brew
if [[ $? != 0 ]] ; then
    echo "Homebrew is not installed. You may be asked for your password."
    echo "Installing Homebrew..."
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    echo "Homebrew is installed."
fi

echo "Installing dependencies..."

brew install python

pip install matplotlib pandas pillow pprint numpy scipy pyvisa pyserial beautifulsoup4 aardvark_py
pip install subprocess.run

echo "Dependencies installed."

