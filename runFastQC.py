"""
This script runs the FastQC step of SeqQC. The script opens a
process with the correct parameters.
"""

import shlex
import subprocess as sp
import argparse

def parse_command_line():
    """
    Parser of command line arguments for SeqQC.py
    """
    description = ("This script runs the FastQC step of SeqQC")

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-i", "--indir", default='',
                        help="Directory containing input FastQ files to scan "
                        "(ignored if -f/--files flag is prsent)")
    parser.add_argument("-f", "--files", nargs='*',
                        help="Flag to pass individual files rather than input "
                        "directory.")
    parser.add_argument("-o", "--outdir", default='',
                        help="Output directory")
    parser.add_argument("--tmpdir", default='',
                        help="Temp directory")
    parser.add_argument("-t", "--threads", type=int, default='0',
                        help="Number of threads for FastQC use. Normal use: "
                        "Number of threads = number of files. Default 0 for "
                        "automatic calculation.")

    return parser.parse_args()

def run_fqc(arglist):
    """
    Create and run subprocess for fastqc
    """
    command = "fastqc -o {0} -d {1} -t {2} --extract {3}".format(arglist.fqcdir,
                             arglist.tmpdir, arglist.threads, ' '.join(arglist.files))

    cmdargs = shlex.split(command)
    print(command)
    print(cmdargs)

    p = sp.Popen(cmdargs)
    #p = sp.Popen('date')

    return p

def main(arglist):
    """
    Main function to run standalone FastQC instance
    """
    print("Hello!")
    print(arglist)
    run_fqc(args)

if __name__ == "__main__":

    args = parse_command_line()
    main(args)
