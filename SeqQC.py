"""
This script performs the Sequence Quality Control step of the Cancer
Genome Variant pipeline, controlling the processes and
decision making for each step.
"""

import glob
import datetime
import os
import argparse
import runFastQC as rfqc
import checkFastQC as cfqc
import runTrim as rt

# class SeqQCRunner(object):
#     def __init__ (self, infile, args):
#         adaptrim = False
#         qctrim = False

#     def run_fastqc(self):
#         pass

#     def run_qctrim(self):
#         pass

#     def run_adaptrim(self):
#         pass

#     def check_qc(self):
#         pass

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
    parser.add_argument("-a", "--adaptseq", type=str, default='',
                        help="The adapter sequence to be trimmed from the "
                        "FastQ file.")
    parser.add_argument("-w", "--walltime", default='02:00:00',
                        help="Walltime for PBS submission script. Must be of "
                        "the format hh:mm:ss.")
    return parser.parse_args()

def make_paths(arglist):
    """
    Create paths required for first run of SeqQC pipeline
    """
    arglist.tmpdir = "{0}/tmp".format(arglist.outdir)
    arglist.fqcdir1 = "{0}/FastQC_out/1stpass".format(arglist.outdir)
    arglist.fqcdir2 = "{0}/FastQC_out/2ndpass".format(arglist.outdir)
    arglist.trimdir = "{0}/Trim_out".format(arglist.outdir)
    for dirpath in [arglist.tmpdir, arglist.fqcdir1, arglist.fqcdir1,
                                arglist.trimdir, arglist.outdir]:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
    return arglist

def get_files(arglist):
    """
    Search for and return list of files to pass through SeqQC pipeline
    """
    if not arglist.files:
        infiles = glob.glob('{0}/*fastq*'.format(arglist.indir))
        return infiles
    else:
        ### MAKE SURE NAMED FILES EXIST!!!
        return arglist.files



def get_threads(arglist):
    """
    Find number of threads, either from argparse or number of files.
    """
    if arglist.threads == 0:
        print(len(arglist.files))
        return len(arglist.files)
    else: return arglist.threads


if __name__ == "__main__":

    args = parse_command_line()
    print(args)
    args = make_paths(args)
    args.files = get_files(args)
    args.threads = get_threads(args)
    print(args.files)
    print(args.threads)
    print(args)

    ### Run FastQC
    startrfqc = datetime.datetime.now()
    pfqc = rfqc.run_fqc(args, args.fqcdir1)
    pfqc.wait()
    endrfqc = datetime.datetime.now()
    print(endrfqc-startrfqc)

    ### Run Adapter Trimming
    ptrima = rt.trimadapt(args)
    ptrima.wait()
    ### Check FastQC output, simple yes/no to quality trimming
    passthrough = 1
    qcpass, retrim, recheck = cfqc.check_qc(args, args.fqcdir1, passthrough)

    ### Run Quality Trimming
    if qcpass:
        if retrim:
            ptrimqc = rt.trimQC(args)
            ptrimqc.wait()

        if recheck:
            pfqc = rfqc.run_fqc(args, args.fqcdir2)
            pfqc.wait()
            qcpass, retrim, recheck = cfqc.check_qc(args, args.fqcdir2,
                                                            passthrough)

        ##If qcpass is still true, then finished succesfully.
        if qcpass:
            print "Finished successfully"
        else:
            print "Needs manual check"
    else:
        print "Needs manual check"
