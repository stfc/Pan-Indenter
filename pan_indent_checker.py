#!/usr/bin/env python

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
import os
import re
import sys

from colorama import Fore, Style, init as colorama_init


# Command line Debugging
DEBUG_LINE = Fore.CYAN + "%-16s %3s " + Fore.MAGENTA + "|" + Fore.YELLOW + " %s" + Fore.RESET
DEBUG_DIVIDER = Style.DIM + '-' * 100 + Style.NORMAL

# Indentation to use when formatting
INDENT = '    '

RE_ANNOTATION = re.compile(r'@\w*{.*?}', re.S)
RE_COMMENT = re.compile(r'(?:#|@{.*?}).*')
RE_STRING = re.compile(r'''('.*?'|".*?"(?<!\\"))''')


def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True


def _print_debug(k, v, c=""):
    print(DEBUG_LINE % (k, c[:3], v))


def find_annotation_blocks(text):
    """Find multi-line annotation blocks in a block of text"""
    result = []
    annotations = RE_ANNOTATION.finditer(text)
    for annotation in annotations:
        start_char, end_char = annotation.span()
        start_line = text[:start_char].count('\n') + 1
        end_line = start_line + text[start_char:end_char].count('\n')
        result += range(start_line, end_line + 1)
    return result


def main():
    failedlines = 0

    # Arg parser settings for commandlines
    parser = argparse.ArgumentParser(description='Indent Checker')
    parser.add_argument('action', type=str, choices=['check', 'reformat'], help='Action to perform')
    parser.add_argument('input', type=str, help='Input File')
    parser.add_argument('-o', '--output', type=str, help='Output File')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')

    args = parser.parse_args()
    file_output = None
    if args.output:
        file_output = open(args.output, 'w+')
    else:
        file_output = sys.stdout
    indent_level = 0

    colorama_init(strip=(not supports_color()))

    with open(args.input, 'r+') as file_input:
        print(args.input)
        # Find annotations and reset pointer
        annotations = find_annotation_blocks(file_input.read())
        file_input.seek(0)

        # Iterate over lines
        for line_number, line_raw in enumerate(file_input, 1):
            in_annotation = line_number in annotations

            # Command line Debugging
            if args.debug:
                print(DEBUG_DIVIDER)
                debug_comment = ""
                if in_annotation:
                    debug_comment = "A"
                _print_debug("Line Number ", line_number, debug_comment)
                _print_debug("Indent Level", indent_level, debug_comment)
                _print_debug("Unedited line", line_raw.rstrip(), debug_comment)

            line_old = line_raw.rstrip()
            line_new = line_old
            line_stripped = line_raw.strip()
            indent_change = 0

            if not in_annotation:
                # Determine whether to send the line forwards or backwards for formatting
                cleanline = RE_STRING.sub("'IGNORED_STRING'", line_stripped)
                cleanline = RE_COMMENT.sub('# IGNORED COMMENT', cleanline)
                startmatch = re.findall(r'[{(]', cleanline)
                endmatch = re.findall(r'[})]', cleanline)
                curlyout = re.search(r'(^[)}])(.*)([{(]$)', cleanline)
                if args.debug:
                    _print_debug("Cleaned line", cleanline)


                # Set the direction to send the line
                if len(endmatch) > len(startmatch):
                    indent_change = -1

                if len(startmatch) > len(endmatch):
                    indent_change = 1

                if args.debug:
                    _print_debug("Indent Change", indent_change)

                # Apply indent reductions before printing
                if indent_change < 0:
                    indent_level += indent_change

                if curlyout:
                    indent_level += -1

                line_new = (INDENT * indent_level) + line_stripped
                line_new = line_new.rstrip()

            if args.debug:
                _print_debug("Edited Line", line_new, debug_comment)

            # Write output
            if args.action == 'reformat' and file_output:
                file_output.write(line_new + "\n")
                file_output.flush()

            elif args.action == 'check':
                if line_new != line_old:
                    failedlines += 1
                    if args.action == 'check':
                        print(("%3d:" % line_number) + Fore.RED + ("%s" % line_old) + Fore.RESET)
                        print(("%3d:" % line_number) + Fore.GREEN + ("%s" % line_new) + Fore.RESET)
                        print("")

            if not in_annotation:
                # Apply indent increases after printing
                if indent_change > 0:
                    indent_level += indent_change

                if curlyout:
                    indent_level += 1

            if args.debug:
                _print_debug("Ending Indent", indent_level, debug_comment)

    if failedlines:
        if args.action == 'check':
            print("Found %d lines with incorrect indentation." % failedlines)
        sys.exit(1)
    else:
        if args.action == 'check':
            print("No problems found.")
        sys.exit(0)


if __name__ == '__main__':
    main()
