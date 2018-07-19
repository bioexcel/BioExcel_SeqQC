#!/usr/bin/env python

"""
This script runs the FastQC step of SeqQC. The script opens a
FastQC process with the correct parameters.
"""
import os
import runFastQC as rfqc
import runTrim as rt
import seqqcUtils as sqcu

def readQCreports(fqcout):
    """
    Read in QC reports for each of the files provided
    """
    reports = []
    fqcdirs = [os.path.join(fqcout, o) for o in os.listdir(fqcout) if
                                os.path.isdir(os.path.join(fqcout, o))]
    for fqcdir in fqcdirs:
        summaryfile = "{0}/summary.txt".format(fqcdir)
        with open(summaryfile) as f:
            qcsumm = f.readlines()
        reports.append(qcsumm)
    return reports

def get_qc(fqcdir, passthrough):
    """
    Returns QC flags for both samples
    """
    #Default to assuming things are fine and dandy, change if not.
    qcpass = True
    qtrim = False
    atrim = False
    recheck = False
    reports = readQCreports(fqcdir)

    #Run through the summaries step by step, and apply flags as needed
    #Hopefully will be easier to alter in future versions (config file?)
    for report in reports:
        qclist = []
        for line in report:
            splitline = line.split()
            qclist.append(splitline[0]) #Store Pass/Warn/Fail in list

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


def check_qc(arglist):
    """
    Check the QC reports for any pass/fails, and use these to decide
    whether to run a QC trim on the samples. True = Pass, False = Fail, trim
    needed.
    """
    ### First pass through this part of the workflow, different options for
    ### pass dealt with in get_qc - may need changing if logic changes
    passthrough = 1
    qcpass, qtrim, atrim, recheck = get_qc(arglist.fqcdir1, passthrough)
    if qcpass:

        if qtrim and atrim:
            ### Do both quality AND adapter trimming
            ptrimfull, f1, f2 = rt.trimFull(arglist, arglist.files)
            ptrimfull.wait()
        else:
            if qtrim:
                ### Run quality trimming only
                ptrimqc, f1, f2 = rt.trimQC(arglist, arglist.files)
                ptrimqc.wait()

            if atrim:
                ### Run adapter trimming only
                ptrima, f1, f2 = rt.trimAdapt(arglist, arglist.files)
                ptrima.wait()

        if recheck:
            ### May need work if logic changes to need retrim after pass 2
            passthrough = 2
            pfqc = rfqc.run_fqc(arglist, arglist.fqcdir2, [f1, f2])
            pfqc.wait()
            qcpass, qtrim, atrim, recheck = get_qc(arglist.fqcdir2,
                                                           passthrough)

        ##If qcpass is still true, then finished succesfully.
        if qcpass:
            print("Finished successfully")
            print(qcpass, qtrim, atrim, recheck)

        else:
            print("Needs manual check")
            print(qcpass, qtrim, atrim, recheck)
    else:
        print("Needs manual check")
        print(qcpass, qtrim, atrim, recheck)


if __name__ == "__main__":
    description = ("This script checks FastQC output for PASS/WARN/FAIL values")
    args = sqcu.parse_command_line(description)

    args = sqcu.make_paths(args)
    args.files = sqcu.get_files(args)

    ### Check FastQC output, simple yes/no to quality trimming
    ### Output and resubmission of jobs handled by checkFastQC
    check_qc(args)
