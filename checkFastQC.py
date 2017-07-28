#!/usr/bin/env python

"""
This script runs the FastQC step of SeqQC. The script opens a
FastQC process with the correct parameters.
"""
import os
import argparse


# import argparse

# def parse_command_line():
#     """
#     Parser of command line arguments for SeqQC.py
#     """
#     description = ("This script runs the FastQC step of SeqQC")

#     parser = argparse.ArgumentParser(
#         description=description,
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

#     parser.add_argument("-i", "--fqcdir", default='',
#                         help="Directory containing input FastQ files to scan "
#                         "(ignored if -f/--files flag is prsent)")
#     parser.add_argument("-f", "--files", nargs='*',
#                         help="Flag to pass individual files rather than input "
#                         "directory.")
#     parser.add_argument("-o", "--fqcdir", default='',
#                         help="Output directory")
#     parser.add_argument("--tmpdir", default='',
#                         help="Temp directory")
#     parser.add_argument("-t", "--threads", type=int, default='0',
#                         help="Number of threads for FastQC use. Normal use: "
#                         "Number of threads = number of files. Default 0 for "
#                         "automatic calculation.")

#     return parser.parse_args()

# class FastQCCheck(object):
#     '''
#     Class for reading and checking FastQC reports
#     '''
#     def __init__(self, arglist, infile):
#         self.infile = infile
#         self.arglist = arglist
#         self.passthrough = 1
#         self.qcdict = dict.fromkeys(["basic", "baseq"])
#         self.basic, self.baseq, self.tileq, self.seqq

#     def readQCreport(self):
#         '''
#         Read in QC report for the file provided
#         '''
#         _, filename = os.path.split(self.infile)
#         summaryfile = "{0}/{1}/summary.txt".format(fqcdir,
#                         filename.replace('.fastq.bz2', '_fastqc'))
#         with open(summaryfile) as f:
#             self.basic = f.readline.split()[0]

#             # for line in f:
#             #     splitline = line.split()

#     def printargs(self):
#         '''Print args for object'''
#         print self.arglist

#     def printfile(self):
#         '''Print file creating object'''
#         print self.infile


def parse_command_line(desc=("This script performs the Sequence "
                "Quality Control step of the Cancer Genome Variant pipeline.")):
    """
    Parser of command line arguments for SeqQC.py
    """


    parser = argparse.ArgumentParser(
        description=desc,
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
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="Run through stages without actually creating "
                        "new processes.")
    return parser.parse_args()

def readQCreports(fqcout):
    '''
    Read in QC reports for each of the files provided
    '''
    reports = []
    fqcdirs = [os.path.join(fqcout, o) for o in os.listdir(fqcout) if
                                os.path.isdir(os.path.join(fqcout, o))]
    for fqcdir in fqcdirs:
        summaryfile = "{0}/summary.txt".format(fqcdir)
        with open(summaryfile) as f:
            qcsumm = f.readlines()
        reports.append(qcsumm)
    return reports

def printlog(qcpass, qtrim, recheck):
    '''
    Print things to a log file
    '''
    print qcpass, qtrim, recheck
    # Pring things to a log file.
    return

def check_qc(fqcdir, passthrough):
    '''
    Check the QC reports for any pass/fails, and use these to decide
    whether to run a QC trim on the samples. True = Pass, False = Fail, trim
    needed.
    '''
    #Default to assuming things are fine and dandy, change if not.
    qcpass = True
    qtrim = False
    atrim = False
    recheck = False
    reports = readQCreports(fqcdir)
    #print "Hello?"
    for report in reports:
        qclist = []
        for line in report:
            splitline = line.split()
            qclist.append(splitline[0])

        if qclist[0] != 'PASS':
            qcpass = False

        if qclist[1] != 'PASS' and passthrough == 1:
            qtrim = True

        if qclist[2] != 'PASS' and passthrough == 1:
            qtrim = True

        if qclist[3] != 'PASS':
            qcpass = False

        if qclist[4] == 'FAIL':
            if passthrough == 1:
                qtrim = True
                recheck = True
            if passthrough == 2:
                qcpass = False

        if qclist[5] == 'FAIL':
            qcpass = False

        if qclist[6] != 'PASS':
            qcpass = False

        if qclist[7] != 'PASS' and passthrough == 1:
            qcpass = False

        if qclist[8] != 'PASS':
            qcpass = False

        if qclist[9] != 'PASS' and passthrough == 1:
            atrim = True
            recheck = True
        if qclist[9] == 'FAIL' and passthrough == 2:
            qcpass = False

        if qclist[10] != 'PASS':
            if passthrough == 1:
                atrim = True
                recheck = True
            if passthrough == 2:
                qcpass = False            

        if qclist[11] != 'PASS' and passthrough == 1:
            qtrim = True
            recheck = True
        if qclist[11] == 'FAIL' and passthrough == 2:
            qcpass = False

    return qcpass, qtrim, atrim, recheck

def main(arglist):
    """
    Main function to run standalone FastQC instance
    """
    print("Hello!")
    print(arglist)
    qcpass, qtrim, atrim, recheck = check_qc(args.indir, 1)
    print qcpass, qtrim, atrim, recheck
    #run_fqc(args)

if __name__ == "__main__":
    description = ("This script checks FastQC output for PASS/WARN/FAIL values")
    args = parse_command_line(description)
    main(args)
