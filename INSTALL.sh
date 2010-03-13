#!/bin/sh

py_compilefiles scrabblehack.py
mv scrabblehack.pyc scrabblehack
chmod +x scrabblehack
echo "Installing scrabblehack in /usr/bin..."
sudo cp scrabblehack /usr/bin
rm scrabblehack
echo "Done"
