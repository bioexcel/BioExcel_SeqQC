import glob
import subprocess as sp
import datetime
import shlex
import os, sys
import argparse
import SeqQC

class MyFormatter(argparse.HelpFormatter):
    def __init__(self,prog):
        super(MyFormatter,self).__init__(prog,max_help_position=37)

def parse_command_line():

    description = ("This script submits the job required to perform the "
                    "Sequence Quality Control step of the Cancer Genome "
                    "Variant pipeline.")

    parser = argparse.ArgumentParser(
        description = description,
        formatter_class = MyFormatter)
        #formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    
    parser.add_argument("-o", "--outdir", default='./',
                        help="Output directory")
    parser.add_argument("-t", "--threads", type=int, default='0',
                        help="Number of threads for FastQC use. Normal use: "
                        "no. of threads = no. of files. Default 0 for "
                        "automatic calculation.")
    parser.add_argument("-w", "--walltime", default='02:00:00',
                        help="Walltime for PBS submission script. Must be of "
                        "the format hh:mm:ss.")
    parser.add_argument("-i", "--indir", default='./',
                        help="Directory of input FastQ files to scan (ignored "   
                        "if -f/--files flag is present)")
    parser.add_argument("-f", dest='files', nargs='*',
                        help="Flag to pass individual files rather than input "
                        "directory.")

    return parser.parse_args()

def make_command(args):
    args.command = "python {0}/SeqQC.py -o {1} -t {2} -f {3} ".format(sys.path[0], 
                                    args.outdir, args.threads, ' '.join(args.files))

def write_job(args):
    with open(os.path.join(sys.path[0], 'template.job'),'r') as f:
        job = f.read().format(args.threads,args.walltime,args.outdir,args.command)
    args.jobfile = "{0}/SeqQC.job".format(args.outdir)
    with open(args.jobfile,'w') as fo:
        fo.write(job)

def submit_job(args):
    cmdstr = "qsub {}".format(args.jobfile)

    cmdargs = shlex.split(cmdstr)
    print(cmdstr)
    #print(cmdargs)

    p = sp.Popen(cmdargs)
    p = sp.Popen('date')

if __name__ == "__main__":

    args = parse_command_line()
    args = SeqQC.make_paths(args)
    args.files = SeqQC.get_files(args)
    make_command(args)
    write_job(args)
    submit_job(args)