#!/usr/bin/env python

"""
This script contains several utility functions for use with the SeqQC portion
of the IGMM Cancer Genome Sequencing workflow developed as part of BioExcel
"""

import glob
import os
import sys

def make_paths(arglist):
    """
    Create paths required for run of SeqQC pipeline
    """
    arglist.tmpdir = os.path.abspath("{0}/tmp".format(arglist.outdir))
    arglist.fqcdir1 = os.path.abspath("{0}/FastQC_out/1stpass".format(
                                                            arglist.outdir))
    arglist.fqcdir2 = os.path.abspath("{0}/FastQC_out/2ndpass".format(
                                                            arglist.outdir))
    arglist.trimdir = os.path.abspath("{0}/Trim_out".format(arglist.outdir))
    arglist.outdir = os.path.abspath(arglist.outdir)
    arglist.indir = os.path.abspath(arglist.indir)

    for dirpath in [arglist.tmpdir, arglist.fqcdir1, arglist.fqcdir2,
                                arglist.trimdir, arglist.outdir]:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
    return arglist

def get_files(arglist):
    """
    Search for and return list of files to pass through SeqQC pipeline
    """
    if not arglist.files:
        # arglist dirs already have abs paths, so don't need to expand
        infiles = glob.glob('{0}/*fastq*'.format(arglist.indir))
    else:
        # make sure files exist
        for checkfile in arglist.files:
            if not os.path.isfile(checkfile):
                print "{} does not exist. Exiting.".format(checkfile)
                sys.exit()
        # expand paths to files (now we know the all exist)
        infiles = [os.path.abspath(x) for x in arglist.files]
    return infiles

def get_threads(arglist):
    """
    Find number of threads, either from argparse or number of files.
    """
    if arglist.threads == 0:
        print(len(arglist.files))
        return len(arglist.files)

    return arglist.threads
    