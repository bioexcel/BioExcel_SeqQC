import shlex
import subprocess as sp
import argparse

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

def run_fqc(args):

    command = "fastqc -o {0} -d {1} -t {2} --extract {3}".format(args.fqcdir,
                             args.tmpdir, args.threads, ' '.join(args.files))

    cmdargs = shlex.split(command)
    print(command)
    print(cmdargs)

    p = sp.Popen(cmdargs)
    #p = sp.Popen('date')

    return p

def main(args):
    '''
    Main function to run standalone FastQC instance
    '''
    print("Hello!")

if __name__ == "__main__":

    args = parse_command_line()
    main(args)
