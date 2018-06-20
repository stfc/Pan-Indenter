#!/usr/bin/env python2

import argparse
import re

DEBUG_LINE = "\033[36m%-16s \033[35m|\033[0m %s"

INDENT = '    '

def _print_debug(k, v):
    print DEBUG_LINE % (k, v)
    #pass

def main():
    parser = argparse.ArgumentParser(description='Indent Checker')
    parser.add_argument('input', type=str, help='Input File')
    parser.add_argument('output', type=str, help='Output File')
    args = parser.parse_args()

    indent_level = 0

    with open(args.input, 'r+') as file_input:
        with open(args.output, 'w+') as file_output:
            for line_number, line in enumerate(file_input):
                print '\033[1;32m-\033[0m' * 100

                _print_debug("Line Number ", line_number)
                _print_debug("Indent Level", indent_level)
                _print_debug("Unedited line", line.rstrip())

                line = line.strip()
                indent_change = 0

                startmatch = re.findall(r'[{(]', line)
                endmatch = re.findall(r'[})]', line)
                if len(endmatch) > len(startmatch):
                    indent_change = -1
                if len(startmatch) > len(endmatch):
                    indent_change = 1
                _print_debug("Indent Change", indent_change)
                if indent_change < 0:
                    indent_level += indent_change
                line = (INDENT * indent_level) + line
                _print_debug("Edited Line ", line)

                file_output.write(line + "\n")
                file_output.flush()

                if indent_change > 0:
                    indent_level += indent_change
                _print_debug("Ending Indent", indent_level)
if __name__ == '__main__':
    main()
