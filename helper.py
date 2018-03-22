def showHelp(scr):
    l = [ "\nRPOGUENG - the testgame\n",
        "\n https://github.com/viileppi/rpogueng \n",
        "You are exploring a previously unknown planet,",
        "which is populated with all sorts of creatures.\n",
        "Your mission is to make the red hostile aliens",
        "non-hostile. This can be accomplished by either",
        "talking to them (press 't') or in some cases",
        "by hitting them... even to the death if needed.\n",
        "To view the map, press 'm'. The map will show",
        "areas you have explored. Areas with hostile ",
        "aliens are shown in red. Press 'q' to quit.\n",
        "Friendly green aliens will give you their HP",
        "if you're wounded and they'll fight for you.\n",
        "To move, use arrow keys or following keyset:\n",
        " y  k  u",
        "  \\ | /",
        "h - @ - l",
        "  / | \\",
        " b  j  n"]
    for line in l:
        scr.addstr(line + "\n")
    scr.refresh()
    scr.getkey()
    scr.clear()
    scr.refresh()
