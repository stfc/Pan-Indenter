"""This Program is for sorting indents in a programs files."""
import re
import argparse
import logging
parser = argparse.ArgumentParser(description='Process some integers.')
logger = logging.getLogger('Testing')
level = logging.DEBUG
parser.add_argument('-i',
                    help='Declare the name of the file being checked',
                    type=argparse.FileType('rt'),
                    required=True)
parser.add_argument('-o',
                    help='Declare outputted files name',
                    type=argparse.FileType('wt'),
                    required=True)
parser.add_argument('-debug', help='Debugging', action="store_true")
try:
    results = parser.parse_args()
except IOError, msg:
    parser.error(str("you probably missed a command, try -h"))
if results.debug:
    logging.basicConfig(level=logging.DEBUG)
DEBUG_LINE = "\033[36m" + '%-16s | %s' + "\033[0m"
file1 = results.i
file2 = results.o
Indentcount = 0
linecount = 0
with file1 as f:
    for line in f:
        logging.debug(DEBUG_LINE % ("Starting Indent", "\033[33m" +
                                    str(Indentcount) + "\033[0m"))
        logging.debug(DEBUG_LINE % ("Unedited line", "\033[37m" +
                                    line.rstrip() + "\033[0m"))
        line = line.strip()
        linecount = linecount + 1
        IndentIncrease = 0
        IndentDecrease = 0
        startmatch = re.findall(r'[{(]', line)
        endmatch = re.findall(r'[})]', line)
#        quoteregex = re.match(
#            r"(?:[\"'].*?[\"'](\s*,\s*)[\"'].*?[\"']|(?:\s*,\s*(?=.*?\s*,\s*))|(?:\s*,\s*(?=.*?\);)))", line) # Code not used for now
        if startmatch:
            IndentIncrease += len(startmatch)
            logging.debug(DEBUG_LINE % ("Found { or (",
                                        "\033[32m" + "Indent increased by: " +
                                        str(IndentIncrease) + "\033[0m"))
        if endmatch:
            IndentDecrease += len(endmatch)
            logging.debug(DEBUG_LINE % ("Found } or )",
                                        "\033[31m" + "Indent decreased by: " +
                                        str(IndentDecrease) + "\033[0m"))

        IndentChange = IndentIncrease - IndentDecrease
#        if quoteregex: # Code not used for now
#            logging.debug(DEBUG_LINE % ("QuoteWorking", "QuoteWorking"))
#            line = re.sub(
#                r"(?:([\"'].*?[\"'])(\s*,\s*)([\"'].*?[\"'])|((?:\s*,\s*(?=.*?\s*,\s*))|(?:\s*,\s*(?=.*?\);))))", r"\1" + ", " + r"\3", line)
        logging.debug(DEBUG_LINE % ("IndentChange",
                                    "\033[37m" + str(IndentChange) + "\033[0m"))
        Indentcount -= IndentDecrease
        if IndentChange >= 0:
            line = ("    " * Indentcount) + line
        Indentcount += IndentIncrease
        if IndentChange < 0:
            line = ("    " * Indentcount) + line
        line += "\n"
        file2.write(line)
        logging.debug(DEBUG_LINE % ("Edited Line ", "\033[37m" +
                                    line + "\033[0m"))
        logging.debug(DEBUG_LINE % ("Line Number ", "\033[34m" +
                                    str(linecount) + "\033[0m"))
        file2.flush()
        logging.debug(DEBUG_LINE % ("Ending Indent", "\033[33m" +
                                    str(Indentcount) + "\033[0m"))
        logging.debug('\033[1;32m-\033[0m' * 100)
quit()
