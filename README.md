# Keyboard lock widget
This widget adds little clickable widget on the qtile bar that locks keyboard using xinput.

## Config

### Mandatory elements
lock\_icon - Path to lock icon (string)\
unlock\_icon - Path to unlock icon (string)\
keyboard\_device\_id - Id of your keyboard in xinput (Look below) (int)\
keyboard\_master\_id - Id of master device that your keyboard is attached to (Look below) (int)\

### Additional elements
scale - Enable/Disable icons scalling (True/False)\
rotate - Rotate icons in degrees counter-clockwise (float)\
margin - Margin inside the box (int)\
margin\_x - X Margin. Overrides margin (int)\
margin\_y - Y Margin. Overrides margin (int)

## How to get ids from xinput
In terminal type xinput list and look at element with name similar to AT Translated Set 2 keyboard. Keyboard id is the number after id= and master id is the number in parentheses[slave keyboard (#)].

## How to use
You can toggle lock by clicking on icon in your bar or use qshell with commands lock, unlock and toggle.
