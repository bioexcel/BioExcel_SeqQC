"""
This script runs the FastQC step of SeqQC. The script opens a
FastQC process with the correct parameters.
"""

import argparse

def parse_command_line():
    """
    Parser of command line arguments for SeqQC.py
    """
    description = ("This script runs the FastQC step of SeqQC")

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

def readQCreports(arglist):
    '''
    Read in QC reports for each of the files provided
    '''
    return 0, 1

def check_qc(arglist):
    '''
    Check the QC reports for any pass/fails, and use these to decide
    whether to run a QC trim on the samples. True = Pass, False = Fail, trim
    needed.
    '''
    r1, r2 = readQCreports(arglist)

    return True

def main(arglist):
    """
    Main function to run standalone FastQC instance
    """
    print("Hello!")
    print(arglist)
    #run_fqc(args)

if __name__ == "__main__":

    args = parse_command_line()
    main(args)
