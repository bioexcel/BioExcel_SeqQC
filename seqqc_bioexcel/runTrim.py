#!/usr/bin/env python

"""
This script runs the Trim step of SeqQC. The script opens a
cutadapt process with the correct parameters.
"""

import shlex
import subprocess as sp
import seqqc_bioexcel.seqqcutils as sqcu

def trimAdapt(arglist, infiles):
    """
    Create and run subprocess for running cutadapt to remove adapter sequences
    from sequencing data.
    """

    in1 = infiles[0]
    in2 = infiles[1]

    out1 = "{0}/ATrimmed1.fq".format(arglist.trimdir)
    out2 = "{0}/ATrimmed2.fq".format(arglist.trimdir)

    command = "cutadapt --format=fastq -a {0} -A {0} -o {1} -p {2} "\
        "{3} {4}".format(arglist.adaptseq, out1, out2, in1, in2)

    cmdargs = shlex.split(command)
    print(command)
    print(cmdargs)

    p = sp.Popen(cmdargs)

    return p, out1, out2


def trimQC(arglist, infiles):
    """
    Create and run subprocess for running cutadapt to remove poor quality
    sequences from sequencing data.
    """

    in1 = infiles[0]
    in2 = infiles[1]

    out1 = "{0}/QCTrimmed1.fq".format(arglist.trimdir)
    out2 = "{0}/QCTrimmed2.fq".format(arglist.trimdir)

    command = "cutadapt --format=fastq -q 20 -o {0} -p {1} {2} {3}".format(out1,
                                                    out2, in1, in2)

    cmdargs = shlex.split(command)
    print(command)
    print(cmdargs)

    p = sp.Popen(cmdargs)

    return p, out1, out2

def trimFull(arglist, infiles):
    """
    Create and run subprocess for running cutadapt to remove poor quality
    sequences from sequencing data.
    """

    in1 = infiles[0]
    in2 = infiles[1]

    out1 = "{0}/Trimmed1.fq".format(arglist.trimdir)
    out2 = "{0}/Trimmed2.fq".format(arglist.trimdir)

    command = "cutadapt --format=fastq -q 20 -a {0} -A {0} -o {1} -p {2} {3}"\
                        " {4}".format(arglist.adaptseq, out1, out2, in1, in2)

    cmdargs = shlex.split(command)
    print(command)
    print(cmdargs)

    p = sp.Popen(cmdargs)

    return p, out1, out2

if __name__ == "__main__":
    description = ("This script runs the Trimming step of SeqQC")
    args = sqcu.parse_command_line(description)
    if args.trim == 'full':
        ptrimfull, f1, f2 = trimFull(args, args.files)
        ptrimfull.wait()
    if args.trim == 'adapt':
        ptrimfull, f1, f2 = trimAdapt(args, args.files)
        ptrimfull.wait()
    if args.trim == 'qual':
        ptrimfull, f1, f2 = trimQC(args, args.files)
        ptrimfull.wait()
        