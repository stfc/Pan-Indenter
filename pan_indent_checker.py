#!/usr/bin/env python2

# Copyright 2018 Science & Technology Facilities Council
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import re
import sys
# Command line Debugging
DEBUG_LINE = "\033[36m%-16s \033[35m|\033[0m %s"

# Indent space to use to format the code
INDENT = '    '

def main():
    failedlines = False
# Arg parser settings for commandlines
    parser = argparse.ArgumentParser(description='Indent Checker')
    parser.add_argument('input', type=str, help='Input File')
    parser.add_argument('-o', '--output', type=str, help='Output File')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging.')
    parser.add_argument('--diff', action='store_true', help='Enable diff showing.')
    args = parser.parse_args()
    if args.output:
        file_output = open(args.output, 'w+')
    else:
        file_output = None
    indent_level = 0

    with open(args.input, 'r+') as file_input:
            for line_number, line in enumerate(file_input):

# Command line Debugging
                if args.debug:
                    print '\033[1;32m-\033[0m' * 100
                    def _print_debug(k, v):
                        print DEBUG_LINE % (k, v)
                else:
                    def _print_debug(k, v):
                        pass
                _print_debug("Line Number ", line_number)
                _print_debug("Indent Level", indent_level)
                _print_debug("Unedited line", line.rstrip())
                oldline = line.rstrip()
# Strips line and resets indent_change
                line = line.strip()
                indent_change = 0

# Used to know when to send a line forward or backwards for formatting
                cleanline = re.sub(r'(#.*$)', ' ', line)
                startmatch = re.findall(r'[{(]', cleanline)
                endmatch = re.findall(r'[})]', cleanline)
                curlyout = re.search(r'(^[)}])(.*)([{(])', cleanline)

# This section is to set the direction to send the line
                if len(endmatch) > len(startmatch):
                    indent_change = -1

                if len(startmatch) > len(endmatch):
                    indent_change = 1

# Command line Debugging
                _print_debug("Indent Change", indent_change)

# This is the section that applies the change
                if indent_change < 0:
                    indent_level += indent_change

                if curlyout:
                    indent_level += -1

                linenew = (INDENT * indent_level) + line
                _print_debug("Edited Line ", line)
                if linenew != oldline:
                    failedlines = False
                    if args.diff:
                        print("")
                        print("Line %-5d:%s" % (line_number, line))
                        print("should be :%s" % linenew)

# Writes to file
                if file_output:
                    file_output.write(linenew + "\n")
                    file_output.flush()

                if indent_change > 0:
                    indent_level += indent_change

                if curlyout:
                    indent_level += 1

# Command line Debugging
                _print_debug("Ending Indent", indent_level)
    if failedlines:
        sys.exit(1)
    else:
        sys.exit(0)
if __name__ == '__main__':
    main()
