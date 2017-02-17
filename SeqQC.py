import glob
import subprocess as sp
import datetime
import shlex
import os
import argparse

def parse_command_line():

    description = ("This script performs the Sequence Quality Control step "
                    "of the Cancer Genome Variant pipeline.")

    parser = argparse.ArgumentParser(
        description = description,
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
    args.tmpdir = "{0}/tmp".format(args.outdir)
    args.fqcdir = "{0}/FastQC_out".format(args.outdir)
    args.trimdir = "{0}/Trim_out".format(args.outdir)
    for dirpath in [args.tmpdir, args.fqcdir, args.trimdir]:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
    return args

def get_files(args):
    if not args.files:
        infiles = glob.glob('{0}/*fastq*'.format(args.indir))
        return infiles
    else: return args.files


def get_threads(args):
    if args.threads == 0:
        print len(args.files)
        return len(args.files)
    else: return args.threads

def run_fqc(args):

    command = "fastqc -o {0} -d {1} -t {2} --extract {3}".format(args.fqcdir,
                             args.tmpdir, args.threads, ' '.join(args.files))

    cmdargs = shlex.split(command)
    print(command)
    print(cmdargs)

    p = sp.Popen(cmdargs)
    #p = sp.Popen('date')

    return p

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
    p = run_fqc(args)
    p.wait()
    endfqc = datetime.datetime.now()
    print(endfqc-startfqc)
