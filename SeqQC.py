import glob
import datetime
import os
import argparse
import runFastQC as fqc

def parse_command_line():
    '''
    Parser of command line arguments for SeqQC.py
    '''
    description = ("This script performs the Sequence Quality Control step "
                    "of the Cancer Genome Variant pipeline.")

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

def make_paths(arglist):
    '''
    Create paths required for first run of SeqQC pipeline
    '''
    arglist.tmpdir = "{0}/tmp".format(arglist.outdir)
    arglist.fqcdir = "{0}/FastQC_out/first".format(arglist.outdir)
    arglist.trimdir = "{0}/Trim_out/first".format(arglist.outdir)
    for dirpath in [arglist.tmpdir, arglist.fqcdir, arglist.trimdir]:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
    return arglist

def get_files(arglist):
    '''
    Search for and return list of files to pass through SeqQC pipeline
    '''
    if not arglist.files:
        infiles = glob.glob('{0}/*fastq*'.format(arglist.indir))
        return infiles
    else:
        ### MAKE SURE NAMED FILES EXISTs
        return arglist.files


def get_threads(arglist):
    '''
    Find number of threads, either from argparse or number of files.
    '''
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
    startfqc = datetime.datetime.now()
    p = fqc.run_fqc(args)
    p.wait()
    endfqc = datetime.datetime.now()
    print(endfqc-startfqc)
