#!/usr/bin/env python3

# Takes an input and prints only the language specified
# Usage: python print-lang.py [filename] [lang-code]
# i.e., python print-lang.py 04.md ru or python print-lang.py 04.md en

import sys
import enchant
from guess_language import guessLanguage

input_file = sys.argv[1]
lang = sys.argv[2]
output_file = (input_file.rsplit(".", 1)[ 0 ]) + "_" + lang + ".md"

myfile = open(input_file,'r',encoding='utf-8')
output_file = open(output_file,'w',encoding='utf-8')

for line in myfile:
  if guessLanguage(line) == lang:
    output_file.write(line + "\n")
  else:
    pass
