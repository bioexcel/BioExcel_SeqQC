#!/usr/bin/env python

"""
This script runs the FastQC step of SeqQC. The script opens a
FastQC process with the correct parameters.
"""

import shlex
import subprocess as sp
import seqqc_bioexcel.seqqcutils as sqcu

def run_fqc(infiles, fqcdir,  tmpdir):
    """
    Create and run subprocess for fastqc
    """
    command = "fastqc -o {0} -d {1} -t 2 --extract {2}".format(fqcdir,
                             tmpdir, ' '.join(infiles))

    cmdargs = shlex.split(command)
    print(command)
    print(cmdargs)

    p = sp.Popen(cmdargs)

    return p

if __name__ == "__main__":
    description = ("This script runs the FastQC step of SeqQC")
    args = sqcu.parse_command_line(description)

    args = sqcu.make_paths(args)
    args.files = sqcu.get_files(args)

    ### Run FastQC
    pfqc = run_fqc(args.fqcdir, args.files, args.tmpdir)
    pfqc.wait()
