#!/usr/bin/env python
#
# Distributed under GPLv2.1 or any later
#
# Copyright (C) 2014 Tomas Gavenciak <gavento@ucw.cz>
# Copyright (C) 2014 Cyril Hrubis <metan@ucw.cz>
#

import re
import getopt
from sys import argv, exit
from os import path, remove, system

DEFAULT_INDENT = 4

def perror(filename, line, lineno, row, error):
    print('%s:%i:%i: error: %s\n' % (filename, lineno, row, error))
    print(line)
    print(' ' * row + '^\n')
    exit(1)

def transform(filename, lines, include_dirs):
    out = []
    lastindent = 0
    lineno = 0

    for l in lines:
        lineno += 1
        l = l.rstrip('\n')
        if l.startswith('@'):
            # lines with '@ end' only decrease the indent
            if re.match('@\s*end\s*', l):
                lastindent -= DEFAULT_INDENT
            elif re.match('@\s*include.*', l):
                include_filename = re.sub('@\s*include\s*', '', l)
                include_path = ''

                if not include_filename:
                    perror(filename, l, lineno, len(l), 'Expected filename')

                for dirname in include_dirs:
                    if path.isfile(dirname + '/' + include_filename):
                        include_path = dirname + '/' + include_filename
                        break

                if not include_path:
                    perror(filename, l, lineno, len(l) - len(include_filename),
                           "Failed to locate '%s' in %s" %
                           (include_filename, include_dirs))

                try:
                    infile = open(include_filename, 'r')
                except Exception as err:
                    perror(filename, l, lineno, len(l) - len(include_filename), str(err))

                out = out + transform(include_filename, infile.readlines(), include_dirs)

                infile.close()
            else:
                code = re.sub('\t', '        ', l[2:]).rstrip()
                # full-line comments do not change last indent
                if code and not re.match('^[ ]*#', code):
                    lastindent = len(code) - len(code.lstrip())
                    if code.endswith(':'):
                        lastindent += DEFAULT_INDENT
                    if re.match('\s*return\s+.*', code):
                        lastindent -= DEFAULT_INDENT
                out.append(code)
        else:
            # escape \ and "
            l = l.replace("\\", "\\\\")
            l = l.replace('"', '\\"')
            # parse {{ expression }} blocks
            tokens = re.split('({{|}})', l)
            code = 'cct_write("'
            row = 0
            in_code = False
            for token in tokens:
                if token == '{{':
                    if in_code:
                        perror(filename, l, lineno, row, 'Unexpected {{')
                    else:
                        in_code = True
                        code = code + '" + str('
                elif token == '}}':
                    if in_code:
                        in_code = False
                        code = code + ') + "'
                    else:
                        perror(filename, l, lineno, row, 'Unexpected }}')
                else:
                    code = code + token

                row += len(token)

            if in_code:
                perror(filename, l, lineno, row, 'Unterminated {{')

            out.append(' ' * lastindent + code + '")')

    return out

header = [
    "#!/usr/bin/env python",
    "#",
    "# Generated file do _not_ edit by hand!",
    "#",
    "from sys import exit",
    "",
]

functions = [
    "def cct_error(string):",
    "    print('cct: error: ' + string)",
    "    exit(1)",
    "",
    "def cct_write(line):",
    "    cct_outfile.write(line)",
    "    cct_outfile.write('\\n')",
    "",
    "try:",
    "    global cct_outfile",
    "    cct_outfile = open(cct_outfile_path, 'w')",
    "except Exception as err:",
    "    cct_error('Failed to open file: ' + cct_outfile_path + ' : ' + str(err))",
    "",
]

footer = [
    "",
    "try:",
    "    cct_outfile.close()",
    "except Exception as err:",
    "    cct_error('Failed to write ' + cct_outfile_path + ' : ' + str(err))",
]

def generate(filename, lines, include_dirs, outfile):
    out = header
    out.append("cct_outfile_path = '%s'" % outfile)
    out.append("")
    out = out + functions
    out = out + transform(filename, lines, include_dirs)
    out = out + footer
    return '\n'.join(out)

def error(error):
    print(error)
    exit(1)

def usage():
    print('Usage:\ncct [-Idir] [-v] [-o outfile] file.c.t\n')
    print('-I\n\tAdds include path(s)')
    print('-o\n\tSets output file')
    print('-v\n\tSets verbose mode')
    print('-c\n\tConfig to be loaded parser globals');
    print('-h | --help\n\tPrints this help.')

def main():
    try:
        opts, args = getopt.getopt(argv[1:], 'c:ho:I:v', ['help'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        exit(1)

    include_dirs = ['.']
    verbose = False
    outfile = ''
    config = ''

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            exit(0)
        elif opt == '-I':
            include_dirs.append(arg)
        elif opt == '-v':
            verbose = True
        elif opt == '-o':
            outfile = arg
        elif opt == '-c':
            config = arg

    if len(args) != 1:
        error('No input files.')

    if not outfile:
        if not args[0].endswith('.t'):
            error('No outfile set and template does not end with .t')

        outfile = args[0][:-2]

    if verbose:
        print("Settings\n--------")
        print("Include Dirs:  %s" % include_dirs)
        print("Config:        %s" % config)
        print("Template File: %s" % args[0])
        print("Output File:   %s" % outfile)

    with open(args[0], 'rt') as f:
        t = generate(args[0], f.readlines(), include_dirs, outfile)

        script_name = outfile + '.py'

        try:
            result = open(script_name, 'w')
        except Exception as err:
            error('Failed to open file: ' + script_name + ' : ' + str(err))

        result.write(t)

        try:
            result.close()
        except Exception as err:
            error('Failed to close file: ' + script_name + ' : ' + str(err))

        system('python ' + script_name)

if __name__ == '__main__':
    main()
