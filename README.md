# New – lookup.py
A script that looks up words, parts of words and also strokes in all dictionaries defined in Plover. Sorts results by stroke length or optionally alphabetically. Verbose (-v) output shows additional information (type of entry, entries overwritten by a dictionary with higher precedence, dictionary the word is found in). Arguments are concatenated, so you can simply type "lookup.py this is" and get results for "this is", not for "this" and "is" separately. Use lookup.py -h for help about all options.

# README

This is a dictionary lookup OS X Automator service for [Plover](https://github.com/openstenoproject/plover).
Also included is a bash script to be called from the Terminal.

For more information see the thread on the [Plover Aviary](http://stenoknight.com/plover/aviary/phpBB3/viewtopic.php?f=14&t=4386&p=6524&hilit=dictionary+lookup#p6524).

# Features

* An Automator workflow service that looks up any word(s) selected in the current application. It searches in all json files that reside in ~/Library/Applicaton\ Support/plover/.
* A bash script  to find either an exact match of the word to look up or all matches that contain the argument string

# Installation

1. Download the .zip (button on the right of this text)
2. Double click "Steno lookup" - if asked if you want to install it, do so.
3. If you have dictionaries outside of the default Plover dictionary path, you might want to create soft links to those into ~/Library/Applicaton\ Support/plover/. Finder aliases unfortunatley don't work - you'll have to use the Terminal and type:
\> ln -s path/to/my/dictionary.json ~/Library/Applicaton\ Support/plover/
4. Plover.app should reside in /Applications/ so the icon displayed for the results will be correct.

# Usage

To use the service, select a word in any app that let's you do so, and open Steno lookup from the app menu/Services/ (it will only show up if there's an active selection available). You may want to assign a keyboard shortcut to Steno lookup in System Preferences->Keyboard–>Shortcuts->Services->Text, so that it will be possible to call it using a Plover dictionary entry.

Tip: I use a dictionary entry like this:

"TK\*L": "{^}{#Alt\_L(Shift\_L(Left))}{#Super\_L(Alt_L(F1))}{#Right}",

My keyboard shortcut for Steno lookup is Cmd+Alt+F1, and this entry selects the last typed word and looks it up (so if you had to fingerspell a word, you just stroke TK\*L to find the correct stroke).

The bash script "dictlook" has some options available:

-x Search only for the exact word. Without this option, the result also contains strokes that contain the word as a substring.

-s The word must be the first in the stroke translation

-e The word must be the last in the stroke translation

If you want to search for a phrase you'll have to use quotes, e.g.

\> dictlook "he was"

It's also possible to use grep inside, this will find all suffixes:

\> dictlook "\"{\\^}.*"
