"""
This script submits the job required to perform the Sequence Quality
Control step of the Cancer Genome Variant pipeline, creating output
folders and job submission scripts as needed
"""

import subprocess as sp
import shlex
import argparse
import os
import sys
import datetime as dt

import SeqQC

class MyFormatter(argparse.HelpFormatter):
    """Class for creating tidier help printout"""
    def __init__(self, prog):
        super(MyFormatter, self).__init__(prog, max_help_position=37)

def parse_command_line():
    """
    Parser of command line arguments for SeqQC.py
    """
    description = ("This script submits the job required to perform the "
                    "Sequence Quality Control step of the Cancer Genome "
                    "Variant pipeline.")

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=MyFormatter)
        #formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-o", "--outdir", default='./',
                        help="Output directory")
    parser.add_argument("-t", "--threads", type=int, default='0',
                        help="Number of threads for FastQC use. Normal use: "
                        "no. of threads = no. of files. Default 0 for "
                        "automatic calculation.")
    parser.add_argument("-w", "--walltime", default='02:00:00',
                        help="Walltime for PBS submission script. Must be of "
                        "the format hh:mm:ss.")
    parser.add_argument("-i", "--indir", default='./',
                        help="Directory of input FastQ files to scan (ignored "
                        "if -f/--files flag is present)")
    parser.add_argument("-f", dest='files', nargs='*',
                        help="Flag to pass individual files rather than input "
                        "directory.")

    return parser.parse_args()


def get_submit_time():
    """
    Function to return datetime string of submission for output folder
    if output jobname is not provided.
    """
    dtnow = dt.datetime.now()
    subtime = "{}{:02d}{:02d}_{:02d}{:02d}{:02d}".format(dtnow.year, dtnow.month,
                dtnow.day, dtnow.hour, dtnow.minute, dtnow.second)

    return subtime

def make_command(arglist):
    """
    Creates the full python command to launch SeqQC.py, including
    command line options.
    """
    arglist.command = "python {0}/SeqQC.py -o {1} -t {2} -f {3} ".format(
                            sys.path[0], arglist.outdir, arglist.threads,
                            ' '.join(arglist.files))
    return arglist

def write_job(arglist):
    """
    Fills in template.job file with required parameters, saves job
    file to be submitted in output directory.
    """
    with open(os.path.join(sys.path[0], 'template.job'), 'r') as f:
        job = f.read().format(arglist.threads, arglist.walltime,
                                    arglist.outdir, arglist.command)
    arglist.jobfile = "{0}/SeqQC.job".format(arglist.outdir)
    with open(arglist.jobfile, 'w') as fo:
        fo.write(job)
    return arglist

def submit_job(arglist):
    """
    Submits job to the PBS queue
    """
    cmdstr = "qsub {}".format(arglist.jobfile)

    cmdargs = shlex.split(cmdstr)
    print(cmdstr)
    #print(cmdargs)

    sp.Popen(cmdargs)
    sp.Popen('date')

if __name__ == "__main__":

    args = parse_command_line()
    args = SeqQC.make_paths(args)
    args.files = SeqQC.get_files(args)
    args = make_command(args)
    args = write_job(args)
    submit_job(args)
