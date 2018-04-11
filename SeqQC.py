#!/usr/bin/env python

"""
This script performs the Sequence Quality Control step of the Cancer
Genome Variant pipeline, controlling the processes and
decision making for each step.
"""

import argparse
import runFastQC as rfqc
import checkFastQC as cfqc
import seqqcUtils as sqcu

def parse_command_line(description=("This script performs the Sequence "
                "Quality Control step of the Cancer Genome Variant pipeline.")):
    """
    Parser of command line arguments for SeqQC.py
    """
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
    parser.add_argument("-t", "--threads", type=int, default='0',
                        help="Number of threads for FastQC use. Normal use: "
                        "Number of threads = number of files. Default 0 for "
                        "automatic calculation.")
    parser.add_argument("-a", "--adaptseq", type=str,
                        default='AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT',
                        help="The adapter sequence to be trimmed from the "
                        "FastQ file.")
    parser.add_argument("-w", "--walltime", default='02:00:00',
                        help="Walltime for PBS submission script. Must be of "
                        "the format hh:mm:ss.")
    # parser.add_argument("-d", "--dryrun", action="store_true",
    #                     help="Run through stages without actually creating "
    #                     "new processes. - NOT IMPLEMENTED YET!")
    return parser.parse_args()

if __name__ == "__main__":

    args = parse_command_line()
    args = sqcu.make_paths(args)
    args.files = sqcu.get_files(args)
    args.threads = sqcu.get_threads(args)

    ### Run FastQC
    pfqc = rfqc.run_fqc(args, args.fqcdir1, args.files)
    pfqc.wait()

    ### Check FastQC output, simple yes/no to quality trimming
    ### Output and resubmission of jobs handled by checkFastQC
    cfqc.check_qc(args)
