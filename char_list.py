import winsound as ws 
from time import *
import random

# initial settings
tone_len = [200, 600, 800]
last_word = [""]
guessed = True
char_type = 26
char_length = 10
rating_mode = 0



def play_char(char):
    str = morsedict[char]
    for i in str:
        if (i == '0'):
            ws.Beep(frequency=500, duration=tone_len[0])
        else:
            ws.Beep(frequency=500, duration=tone_len[1])
    sleep(tone_len[2]/1000)

def create_and_play_word(len) : 
    tmpstr = ""
    for i in range(len):
        num = int(random.uniform(0, char_type))
        tmpstr += chr(ord('A') + num)
    for i in tmpstr:
        play_char(i)
    last_word[0] = tmpstr

def play_template():
    tmp = ["Hello World"]
    r = int(random.uniform(0, len(tmp)))
    for i in tmp[r].replace(" ", "").upper() :
        play_char(i)

def play_10(num = None):
    if (num == None):
        num = int(random.uniform(0,10))
    play_char(str(num))

def play_26(num = None):
    if (num == None):
        num = int(random.uniform(0,26))
    play_char(chr(ord('A') + num))

def play_36():
    r = int(random.uniform(0,36))
    if (r < 26):
        play_26(r)
    else:
        play_10(r-26)

def play_len(num):
    ws.Beep(frequency=500, duration=num)

morsedict = {
    'A' : "01",
    'B' : "1000",
    'C' : "1010",
    'D' : "100",
    'E' : "0",
    'F' : "0010",
    'G' : "110",
    'H' : "0000",
    'I' : "00",
    'J' : '0111',
    'K' : "101",
    'L' : "0100",
    'M' : "11",
    'N' : "10",
    'O' : "111",
    'P' : "0110",
    'Q' : "1101",
    'R' : "010",
    'S' : "000",
    'T' : "1",
    'U' : "001",
    'V' : "0001",
    'W' : "011",
    'X' : "1001",
    'Y' : "1011",
    'Z' : "1100",
    '1' : "01111",
    '2' : "00111",
    '3' : "00011",
    '4' : "00001",
    '5' : "00000",
    '6' : "10000",
    '7' : "11000",
    '8' : "11100",
    '9' : "11110",
    '0' : "11111"
}