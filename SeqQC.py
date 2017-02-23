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

def make_paths(args):
    '''
    Create paths required for first run of SeqQC pipeline
    '''
    args.tmpdir = "{0}/tmp".format(args.outdir)
    args.fqcdir = "{0}/FastQC_out/first".format(args.outdir)
    args.trimdir = "{0}/Trim_out/first".format(args.outdir)
    for dirpath in [args.tmpdir, args.fqcdir, args.trimdir]:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
    return args

def get_files(args):
    '''
    Search for and return list of files to pass through SeqQC pipeline
    '''
    if not args.files:
        infiles = glob.glob('{0}/*fastq*'.format(args.indir))
        return infiles
    else:
        ### MAKE SURE NAMED FILES EXISTs
        return args.files


def get_threads(args):
    '''
    Find number of threads, either from argparse or number of files.
    '''
    if args.threads == 0:
        print(len(args.files))
        return len(args.files)
    else: return args.threads


if __name__ == "__main__":

    args = parse_command_line()
    print(args)
    make_paths(args)
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
