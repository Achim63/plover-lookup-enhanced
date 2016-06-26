#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2016 Achim Siebert
# License: GPL v3.0

import os
import sys
import codecs
import locale
import argparse
import simplejson as json


class LookUp():

    home = ""
    dictFileList = []
    dictList = []
    dictNames = []
    defresult = []
    verbose = False
    findall = False

    def change_quotes(self):
        self.stringToFind = self.stringToFind.replace("’", "'")
        self.stringToFind = self.stringToFind.replace("‘", "'")
        self.stringToFind = self.stringToFind.replace('”', '"')
        self.stringToFind = self.stringToFind.replace('“', '"')
        self.stringToFind = self.stringToFind.replace('„', '"')

    def __init__(self, stringToFind):
        self.stringToFind = stringToFind
        self.change_quotes()
        home = os.path.expanduser("~")
        if self.dictNames == []:
            try:
                infile = open(home + '/Library/Application Support/plover/plover.cfg', 'r')
            except:
                print("No plover.cfg found")
                exit(1)

            for line in infile:
                if line.find('dictionary_file') == 0:
                    start_of_path = line.find(' = ') + 3
                    self.dictFileList.append(str(line[start_of_path:-1]))
            infile.close()

            if self.dictFileList == []:
                print("No dictionaries defined")
                exit(1)

            for dict in self.dictFileList:
                self.dictNames.append(dict[dict.rfind("/")+1:-5])
                with open(dict, 'r') as fp:
                    self.dictList.append(json.load(fp))

    def markDoubled(self, strokedef, dname):
        for x, result in enumerate(self.defresult[:]):
            if result[0] == strokedef:
                self.defresult[x][4] = [dname]

    def find(self):
        if self.findall:
            self.findAll()
        else:
            self.findexact()

    def findexact(self):
        self.defresult = []
        i = 0
        for dict in self.dictList:
            newresult = []
            for strokedef in dict:
                entry = dict[strokedef]
                self.markDoubled(strokedef, self.dictNames[i])
                if entry == self.stringToFind:
                    newresult.append([strokedef, entry, self.dictNames[i], "exact match", []])
                elif entry.lower() == self.stringToFind.lower():
                    newresult.append([strokedef, entry, self.dictNames[i], "entry", []])
                elif self.stringToFind + "{^}" == entry:
                    newresult.append([strokedef, entry, self.dictNames[i], "prefix", []])
                elif (self.stringToFind + "{^}{-|}" == entry) or (self.stringToFind + "{-|}" == entry):
                    newresult.append([strokedef, entry, self.dictNames[i], "capitalize next", []])
                elif "{^}" + self.stringToFind == entry:
                    newresult.append([strokedef, entry, self.dictNames[i], "suffix", []])
                elif ("{^}" + self.stringToFind + "{^}" == entry) or \
                     ("{^" + self.stringToFind + "^}" == entry):
                    newresult.append([strokedef, entry, self.dictNames[i], "infix", []])
            self.defresult = self.defresult + newresult
            i = i + 1

    def findreverse(self):
        self.defresult = []
        i = 0
        for dict in self.dictList:
            for strokedef in dict:
                entry = dict[strokedef]
                self.markDoubled(strokedef, self.dictNames[i])
                if strokedef.lower() == self.stringToFind.lower():
                    self.defresult.append([strokedef, entry, self.dictNames[i], "entry", []])
                elif self.findall and (self.stringToFind.lower() in strokedef.lower()):
                    self.defresult.append([strokedef, entry, self.dictNames[i], "entry", []])
            i = i + 1

    def findAll(self):
        self.defresult = []
        i = 0
        for dict in self.dictList:
            newresult = []
            for strokedef in dict:
                entry = dict[strokedef]
                self.markDoubled(strokedef, self.dictNames[i])
                if self.stringToFind.lower() in entry.lower():
                    newresult.append([strokedef, entry, self.dictNames[i], "entry", []])
                    if self.stringToFind == entry:
                        newresult[-1][3] = "exact match"
                    if entry.endswith("{^}"):
                        newresult[-1][3] = "prefix"
                        if entry.startswith("{^}"):
                            newresult[-1][3] = "infix"
                    if entry.startswith("{^}"):
                        newresult[-1][3] = "suffix"
                    if entry.startswith("{^") and entry.endswith("^}"):
                        newresult[-1][3] = "infix"
            self.defresult = self.defresult + newresult
            i = i + 1

    def sortByLength(self):
        self.defresult = self.sortByStrokeLength(self.defresult)
        self.defresult = self.sortByNumberOfStrokes(self.defresult)

    def sortByStrokeLength(self, resultlist):
        less = []
        equal = []
        greater = []

        if len(resultlist) > 1:
            pivot = len(resultlist[0][0])
            for x in resultlist:
                if len(x[0]) < pivot:
                    less.append(x)
                if len(x[0]) == pivot:
                    equal.append(x)
                if len(x[0]) > pivot:
                    greater.append(x)
            return self.sortByStrokeLength(less)+equal+self.sortByStrokeLength(greater)
        else:
            return resultlist

    def sortByNumberOfStrokes(self, resultlist):
        less = []
        equal = []
        greater = []

        if len(resultlist) > 1:
            pivot = resultlist[0][0].count('/')
            for x in resultlist:
                if x[0].count('/') < pivot:
                    less.append(x)
                if x[0].count('/') == pivot:
                    equal.append(x)
                if x[0].count('/') > pivot:
                    greater.append(x)
            return self.sortByNumberOfStrokes(less)+equal+self.sortByNumberOfStrokes(greater)
        else:
            return resultlist

    def sortAlpha(self):
        self.defresult = sorted(self.defresult, key=lambda mydef: mydef[1].lower())

    def prettyprint(self):
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
        for item in self.defresult:
            if item[4] == []:
                if self.verbose:
                    print(u'{i[0]} – {i[1]} ({i[3]}) – {i[2]}'.format(i=item))
                else:
                    if (item[3] == "exact match") and not self.findall:
                        print(u'{i[0]}'.format(i=item))
                    else:
                        print(u'{i[0]} – {i[1]}'.format(i=item))
            else:
                if self.verbose:
                    print(u'({i[0]} overwritten in {i[4][0]})'.format(i=item))
        if self.verbose:
            print(u'--- {} result(s) in {} dictionaries ---'.format(len(self.defresult), len(self.dictList)))


def main():

    parser = argparse.ArgumentParser(description='Lookup words or strokes in Plover dictionaries')
    parser.add_argument('-a', '--all', default=False, action='store_true',
                        help='list all occurences')
    parser.add_argument('-n', '--nosort', default=False, action='store_true',
                        help='do not sort result by length and number of strokes')
    parser.add_argument('-s', '--sortalpha', default=False, action='store_true',
                        help='sort translations alphabetically')
    parser.add_argument('-r', '--reverse', default=False, action='store_true',
                        help='lookup translation of stroke')
    parser.add_argument('-v', '--verbose', default=False, action='store_true',
                        help='print additional information')
    parser.add_argument('words', nargs='+', help='word(s) to look up')

    theargs = parser.parse_args()

    words = theargs.words
    words = " ".join(words)

    lkUp = LookUp(words)
    lkUp.findall = theargs.all
    if theargs.reverse:
        lkUp.findreverse()
    else:
        lkUp.find()
    if not theargs.nosort and not theargs.sortalpha:
        lkUp.sortByLength()
    if theargs.sortalpha:
        lkUp.sortAlpha()
    lkUp.verbose = theargs.verbose
    lkUp.prettyprint()

if __name__ == '__main__':
    main()
