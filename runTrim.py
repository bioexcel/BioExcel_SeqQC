#!/usr/bin/env python

"""
This script runs the Trim step of SeqQC. The script opens a
cutadapt process with the correct parameters.
"""

import shlex
import subprocess as sp
import SeqQC


# def parse_command_line():
#     """
#     Parser of command line arguments for SeqQC.py
#     """
#     description = ("This script runs the FastQC step of SeqQC")

#     parser = argparse.ArgumentParser(
#         description=description,
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

#     parser.add_argument("-i", "--indir", default='',
#                         help="Directory containing input FastQ files to scan "
#                         "(ignored if -f/--files flag is prsent)")
#     parser.add_argument("-f", "--files", nargs='*',
#                         help="Flag to pass individual files rather than input "
#                         "directory.")
#     parser.add_argument("-o", "--outdir", default='',
#                         help="Output directory")
#     parser.add_argument("--tmpdir", default='',
#                         help="Temp directory")
#     parser.add_argument("-t", "--threads", type=int, default='0',
#                         help="Number of threads for FastQC use. Normal use: "
#                         "Number of threads = number of files. Default 0 for "
#                         "automatic calculation.")
#     parser.add_argument("-a", "--adaptseq", type=str, default='',
#                         help="The adapter sequence to be trimmed from the "
#                         "FastQ file.")

#     return parser.parse_args()

def trimadapt(arglist):
    """
    Create and run subprocess for running cutadapt to remove adapter sequences
    from sequencing data.
    """

    in1 = arglist.files[0]
    in2 = arglist.files[1]

    out1 = "{0}/Trimmed1.fq".format(arglist.trimdir)
    out2 = "{0}/Trimmed2.fq".format(arglist.trimdir)

    command = "cutadapt --format=fastq -a {0} -A {0} -o {1} -p {2} "\
        "{3} {4}".format(arglist.adaptseq, out1, out2, in1, in2)

    cmdargs = shlex.split(command)
    print(command)
    print(cmdargs)

    p = sp.Popen(cmdargs)
    #p = sp.Popen('date')

    return p


def trimQC(arglist):
    """
    Create and run subprocess for running cutadapt to remove poor quality
    sequences from sequencing data.
    """

    in1 = "{0}/Trimmed1.fq".format(arglist.trimdir)
    in2 = "{0}/Trimmed2.fq".format(arglist.trimdir)

    out1 = "{0}/QCTrimmed1.fq".format(arglist.trimdir)
    out2 = "{0}/QCTrimmed2.fq".format(arglist.trimdir)

    command = "cutadapt -q 20 -o {0} -p {1} {2} {3}".format(out1, out2,
                                                        in1, in2)

    cmdargs = shlex.split(command)
    print(command)
    print(cmdargs)

    p = sp.Popen(cmdargs)

    return p

def main(arglist):
    """
    Main function to run standalone FastQC instance
    """
    print("Hello!")
    print(arglist)
    #run_fqc(args)

if __name__ == "__main__":
    description = ("This script runs the Trimming step of SeqQC")
    args = SeqQC.parse_command_line(description)
    main(args)
