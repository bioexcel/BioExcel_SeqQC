#!/usr/bin/env python

"""
This script contains several utility functions for use with the SeqQC portion
of the IGMM Cancer Genome Sequencing workflow developed as part of BioExcel
"""

import os
import sys
import argparse
from argparse import HelpFormatter
import shutil
import yaml

class MyFormatter(HelpFormatter):
    """
        From: https://stackoverflow.com/questions/9642692/argparse-help-without-duplicate-allcaps
    """

    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_optional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar

        else:
            parts = []

            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(action.option_strings)

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append(option_string)

                return '%s %s' % (', '.join(parts), args_string)

            return ', '.join(parts)

    def _get_default_metavar_for_optional(self, action):
        return action.dest.upper()

def parse_command_line(description):
    """
    Parser of command line arguments for SeqQC.py
    """
    parser = argparse.ArgumentParser(description=description,
                                                    formatter_class=MyFormatter)

    maingroup = parser.add_argument_group('Main Pipeline',
                    'Main arguments used when running pipeline.')
    maingroup.add_argument("-f", "--files", nargs=2, metavar=('F1', 'F1'),
                            help="Pair of input FastQ files.")
    maingroup.add_argument("-o", "--outdir", default='./', metavar='PATH',
                        help="Output directory. (default: current directory)")
    maingroup.add_argument("--tmpdir", metavar='PATH', help="Temp directory. "
                                    "(default: system tmp location)")
    maingroup.add_argument("-t", "--threads", default=2, type=int, metavar='T',
                        help="Max number of threads to use. NOTE: not all"
                        "stages use all threads. (default: 2)")
    maingroup.add_argument("-a", "--adaptseq", type=str, metavar='ADAP',
        default='AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT',
                    help="The adapter sequence to be trimmed from the "
                    "FastQ file. (default: Illumina TruSeq Universal Adapter)")
    maingroup.add_argument("-q", "--qcconf", type=str, metavar='QCFILE',
                 help="Location of config file. (default: internal config)")

    trimgroup = parser.add_argument_group('Individual Trim stage',
        'Additional arguments used when running the trim stage manually '
        'with: python -m bioexcel_seqqc.runtrim <args>')
    trimgroup.add_argument("--trim", type=str, default='full',
                        choices=['F', 'A', 'Q'],
                        help="The type of trimming to be done on the paired "
                        "sequences: [A]dapter or [Q]uality trimming, "
                        "or [F]ull/both. "
                        "WARNING: For standalone execution of runtrim only! "
                        "(default: [F]ull)")

    printgroup = parser.add_argument_group('Configuration file',
                    'Flags to output example configuration files.')
    printgroup.add_argument("-p", "--printconfig", action='store_true',
                        help="Print example config files to current directory.")

    args = parser.parse_args()
    if args.printconfig:
        return args
    else:
        if not args.files:
            sys.exit("\nusage: bioexcel_seqqc -h for help \n\nbioexcel_seqqc: "
                    "error: the following arguments are required: -f/--files")

    if args.tmpdir:
        args.tmpdir = os.path.abspath(args.tmpdir)
    args.outdir = os.path.abspath(args.outdir)
    args.fqcdir = os.path.abspath("{0}/FastQC_out".format(args.outdir))
    args.trimdir = os.path.abspath("{0}/Trim_out".format(args.outdir))

    return args

def make_paths(dirpath):
    """
    Create paths required for run of SeqQC pipeline
    """
    if not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    return

def get_files(arglist):
    """
    Return list of files to pass through SeqQC pipeline, throws error
    """

    # make sure files exist
    for checkfile in arglist.files:
        if not os.path.isfile(checkfile):
            sys.exit("Error: Input file {} does not exist.".format(checkfile))
    # expand paths to files (now we know the all exist)
    infiles = [os.path.abspath(x) for x in arglist.files]
    return infiles

def get_qcconfig(configfile):
    """
    Read decision configuration of CheckFastQC portion of workflow
    """
    if not configfile: # Read internal file
        basepath = (os.path.dirname(__file__))
        config = yaml.safe_load(open(basepath+'/checkQC.yml'))
    else:
        config = yaml.safe_load(open(configfile))
    return config

def print_config():
    """
    Print/copy decision configuration of CheckFastQC portion of workflow
    """
    basepath = (os.path.dirname(__file__))
    config = basepath+'/checkQC.yml'
    shutil.copy(config, './')
