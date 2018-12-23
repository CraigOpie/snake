#!/usr/bin/env python3
"""
author = "Craig Opie"
author_email = "craigopie@gmail.com"
name = "snake"
version = "1.0.0"
description = "A simple snake game using curser."

"""

import curses
import random
import xml.etree.ElementTree as ET

tree = ET.parse("leader.xml")
root = tree.getroot()

for name in root.iter("name"):
	xmlname = str(name.text)

for score in root.iter("score"):
	xmlscore = str(score.text)

class user(object):

    username = None
    score = 0

    def __init__(self, uname, level):
        self.username = uname
        self.score = level

    def __str__(self):
        return str(self.username) + "_" + str(self.score)

    def __levelup__(self):
        level = int(self.score) + 1
        uname = self.username
        return user(uname, level)

print("High score: "+str(xmlname)+" - "+str(xmlscore))
uname = input("Enter your username: ").replace(" ", "")
level = 0
player = user(uname, level)

s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

snk_x = sw//4
snk_y = sh//2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

food = [sh//2, sw//2]
w.addch(food[0], food[1], curses.ACS_DIAMOND)

key = curses.KEY_RIGHT

loop_condition = True
while loop_condition:
    next_key = w.getch()
    key = key if next_key == -1 else next_key
    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in \
    snake[1:]:
        if (int(xmlscore) > int(player.score)):
            curses.endwin()
            quit()
            loop_condition = False
            continue
        else:
            doc = open("leader.xml", "w")
            doc.write("""<?xml version="1.0" ?>
<scoreboard>
	<player>
		<name>"""+str(player.username)+"""</name>
		<score>"""+str(player.score)+"""</score>
	</player>
</scoreboard>""")
            doc.close()
            curses.endwin()
            print("Congrats! You beat the high score! "+str(player.username)+" - "+str(player.score))
            quit()
            loop_condition = False
            continue
    else:
        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

    new_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    snake.insert(0, new_head)

    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_DIAMOND)
        player = player.__levelup__()
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')
