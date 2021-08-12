#!/bin/bash
rm pylint.log
#pylint -d E1101 --output-format=text postgre.py >>pylint.log
#pylint -d E1101 --output-format=text tdebug.py >>pylint.log
#pylint -d E1101 --output-format=text twtfguard.py >>pylint.log
pylint -d E1101 --output-format=text utilities.py >>pylint.log
pylint -d E1101 --output-format=text txlrep.py >>pylint.log
pylint -d E1101 --output-format=text paginator.py >>pylint.log
cat pylint.log