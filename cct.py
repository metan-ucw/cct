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

def perror(filename, line, lineno, row, error):
    print('%s:%i:%i: error: %s\n' % (filename, lineno, row, error))
    print(line)
    print(' ' * row + '^\n')
    exit(1)

def transform(filename, lines, include_dirs, startindent, indent_depth):
    out = []
    lastindent = 0
    lineno = 0

    for l in lines:
        lineno += 1
        l = l.rstrip('\n')

        if l == '@':
            continue;

        if re.match('\s*@\s.*', l):
            padd = l[:len(l) - len(l.lstrip())]
            l = l.lstrip()
            # lines with '@ end' ends intent block by setting new indent
            if re.match('@\s*end\s*', l):
                lastindent = len(l[2:]) - len(l[2:].lstrip())
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
                    infile = open(include_path, 'r')
                except Exception as err:
                    perror(filename, l, lineno, len(l) - len(include_filename), str(err))

                out = out + transform(include_filename, infile.readlines(),
                                      include_dirs, lastindent + startindent,
                                      indent_depth)

                infile.close()
            else:
                code = re.sub('\t', '        ', l[2:]).rstrip()
                # full-line comments do not change last indent
                if code and not re.match('^[ ]*#', code):
                    lastindent = len(code) - len(code.lstrip())
                    if code.endswith(':'):
                        lastindent += indent_depth
                    if re.match('\s*return\s+.*', code):
                        lastindent -= indent_depth
                if (padd):
                   out.append(' ' * startindent + 'cct.set_padd("%s")' % padd)
                out.append(' ' * startindent + code)
                if (padd):
                   out.append(' ' * startindent + 'cct.set_padd("")')
        else:
            # parse {{ expression }} blocks
            tokens = re.split('({{|}})', l)
            code = 'cct.write("'
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
                    # escape \ and " but only in verbatim mode
                    if not in_code:
                        token = token.replace("\\", "\\\\").replace('"', '\\"')
                    code = code + token

                row += len(token)

            if in_code:
                perror(filename, l, lineno, row, 'Unterminated {{')

            out.append(' ' * (lastindent + startindent) + code + '")')

    return out

header = [
    "#!/usr/bin/env python",
    "#",
    "# Generated file do _not_ edit by hand!",
    "#",
    "from sys import exit",
    "from os import remove, path",
    "",
    "class cct:",
    "    def __init__(self, outfile_path, filename):",
    "        self.first = True",
    "        self.filename = filename",
    "        self.outfile_path = outfile_path",
    "        self.padd = ''",
    "        try:",
    "            self.outfile = open(outfile_path, 'w')",
    "        except Exception as err:",
    "            self.error('Failed to open file: ' + outfile_path + ' : ' + str(err))",
    "",
    "    def error_cleanup(self):",
    "        self.outfile.close()",
    "        remove(self.outfile_path)",
    "",
    "    def error(self, string):",
    "        self.error_cleanup()",
    "        print('cct: error: ' + string)",
    "        exit(1)",
    "",
    "    def write(self, line):",
    "        if self.first:",
    "            self.first = False",
    "            if 'cct_header' in globals():",
    "                cct_header(path.basename(self.outfile_path), self.filename)",
    "        self.outfile.write(self.padd + line + '\\n')",
    "",
    "    def set_padd(self, padd):",
    "        self.padd = padd",
    "",
    "    def close(self):",
    "        if 'cct_footer' in globals():",
    "            cct_footer(path.basename(self.outfile_path), self.filename)",
    "",
    "        try:",
    "            self.outfile.close()",
    "        except Exception as err:",
    "            self.error('Failed to write ' + self.outfile_path + ' : ' + str(err))",
]


footer = [
    "except Exception:",
    "    cct.error_cleanup()",
    "    raise",
    "cct.close()",
]

def generate(filename, lines, include_dirs, indent_depth, outfile):
    out = header
    out.append("cct = cct('%s', '%s')" % (outfile, filename))
    out.append("try:")
    res = transform(filename, lines, include_dirs, indent_depth, indent_depth)
    out = out + res + footer
    return '\n'.join(out)

def error(error):
    print(error)
    exit(1)

def usage():
    print('Usage:\ncct [-Idir] [-v] [-o outfile] file.c.t\n')
    print('-E\n\tStops at first phase, leaves python script')
    print('-i\n\tSets indenntation depth, default is 4')
    print('-I\n\tAdds include path(s)')
    print('-o\n\tSets output file')
    print('-v\n\tSets verbose mode')
    print('-h | --help\n\tPrints this help.')

def main():
    try:
        opts, args = getopt.getopt(argv[1:], 'Eho:i:I:v', ['help'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        exit(1)

    include_dirs = ['.']
    verbose = False
    outfile = ''
    execute = True
    indent_depth = 4

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            exit(0)
        elif opt == '-i':
            indent_depth = int(arg)
        elif opt == '-I':
            include_dirs.append(arg)
        elif opt == '-v':
            verbose = True
        elif opt == '-o':
            outfile = arg
        elif opt == '-E':
            execute = False

    if len(args) != 1:
        error('No input files.')

    if not outfile:
        if not args[0].endswith('.t'):
            error('No outfile set and template does not end with .t')

        outfile = args[0][:-2]

    if verbose:
        print("Settings\n--------")
        print("Include Dirs:      %s" % include_dirs)
        print("Template File:     %s" % args[0])
        print("Output File:       %s" % outfile)
        print("Indentation Depth: %i" % indent_depth)
        print("")

    with open(args[0], 'rt') as f:
        t = generate(args[0], f.readlines(), include_dirs, indent_depth, outfile)

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

        if execute:
            system('python ' + script_name)
            remove(script_name)

if __name__ == '__main__':
    main()
