# never_trust_me
A very secure encryption program

Version: 1.0.1 License: GNU GPL v3. (see LICENSE.txt)

#### This program comes with no warranty.

## Introduction
This is really simple encryption program designed for fun in 72 hours. Think twice if you want to use it in your own projects for security.

## Install requirements

This program tested on Python 3.x and is not yet fully compatible with Python 2.x. You can still try to run it on Python 2, but it is not recommended.

You can install the python dependencies with:

```sh
pip3 install -r requirements.txt
```
NOTE: If you are on Linux and see that the program doesn't handle the copying operation properly, you may want to run the following commands:

```sh
sudo apt install xsel
reboot
```

## How to use
Open a new terminal and change directory to  "never_trust_me" and run the main file with following command:

```sh
python3 main.py
``` 

## How it works

On the encryption part the program takes two inputs from user. 
A text to encrypt and a key for encrypting the text. If length of the key is less than length of the text, 
it adds the key to itself until it reaches the length of the text (i.e. abcabcabca). 
Then performs an xor operation to text and key's corresponding character as every character has a numeric value. 
Converts the resulting numbers to characters.
As a last step, it rotates rigth each character by its index. 

Decryption part is straightforward. Just does the same things in reverse order. 
Rotates left each character by its index then performs an xor operation.

