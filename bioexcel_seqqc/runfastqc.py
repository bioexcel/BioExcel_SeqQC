#!/usr/bin/env python

"""
This script runs the FastQC step of SeqQC. The script opens a
FastQC process with the correct parameters.
"""

import shlex
import subprocess as sp
import bioexcel_seqqc.seqqcutils as sqcu

def run_fqc(infiles, fqcdir, tmpdir, threads):
    """
    Create and run subprocess for fastqc
    """

    # For efficient use of resources, limit threads to no more than number
    # of infiles. FastQC only uses one thread per file at most.
    if threads < len(infiles):
        fqcthreads = threads
    elif threads >= len(infiles):
        fqcthreads = len(infiles)

    sqcu.make_paths(fqcdir)

    if tmpdir:
        sqcu.make_paths(tmpdir)
        command = "fastqc -o {0} -d {1} -t {2} --extract {3}".format(fqcdir,
                            tmpdir, fqcthreads, ' '.join(infiles))
    else:
        command = "fastqc -o {0} -t {1} --extract {2}".format(fqcdir,
                            fqcthreads, ' '.join(infiles))

    cmdargs = shlex.split(command)

    print("STAGE: Running FastQC")
    print(command)

    p = sp.Popen(cmdargs)

    return p

if __name__ == "__main__":
    description = ("This script runs the FastQC step of SeqQC")
    args = sqcu.parse_command_line(description)

    args.files = sqcu.get_files(args)

    ### Run FastQC
    pfqc = run_fqc(args.fqcdir, args.files, args.tmpdir, args.threads)
    pfqc.wait()
