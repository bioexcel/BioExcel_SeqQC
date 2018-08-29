#!/usr/bin/env python

"""
This script runs the FastQC step of SeqQC. The script opens a
FastQC process with the correct parameters.
"""
import os
import bioexcel_seqqc.runfastqc as rfqc
import bioexcel_seqqc.runtrim as rt
import bioexcel_seqqc.seqqcutils as sqcu

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

def get_qc(fqcdir, passthrough, qcconf):
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
        for line in report:
            splitline = line.split('    ') # This relies on FastQC output not
                                           # changing...
            status = splitline[0]
            section = splitline[1]
            sectvars = qcconf[section]
            #qclist.append(splitline[0]) #Store Pass/Warn/Fail in list

            # Check for dependance on 1st or 2nd pass through
            try:
                sectvars = sectvars[passthrough]
            except KeyError:
                pass

            try:
                statvars = sectvars[status]
                if 'qcpass' in statvars:
                    qcpass = statvars['qcpass']
                if 'qtrim' in statvars:
                    qtrim = statvars['qtrim']
                if 'atrim' in statvars:
                    atrim = statvars['atrim']
                if 'recheck' in statvars:
                    recheck = statvars['qcpass']
            except KeyError:
                pass


    return qcpass, qtrim, atrim, recheck


def check_qc(infiles, fqcdir, trimdir, tmpdir, adaptseq, qcconf):
    """
    Check the QC reports for any pass/fails, and use these to decide
    whether to run a QC trim on the samples. True = Pass, False = Fail, trim
    needed.
    """
    ### First pass through this part of the workflow, different options for
    ### pass dealt with in get_qc - may need changing if logic changes
    passthrough = 'pass1'
    qcpass, qtrim, atrim, recheck = get_qc(fqcdir, passthrough, qcconf)
    if qcpass:

        if qtrim and atrim:
            ### Do both quality AND adapter trimming
            ptrimfull, f1, f2 = rt.trimFull(infiles, trimdir, adaptseq)
            ptrimfull.wait()
        else:
            if qtrim:
                ### Run quality trimming only
                ptrimqc, f1, f2 = rt.trimQC(infiles, trimdir)
                ptrimqc.wait()

            if atrim:
                ### Run adapter trimming only
                ptrima, f1, f2 = rt.trimAdapt(infiles, trimdir, adaptseq)
                ptrima.wait()

        if recheck:
            ### May need work if logic changes to need retrim after pass 2
            passthrough = 'pass2'
            pfqc = rfqc.run_fqc([f1, f2], fqcdir+'2ndpass', tmpdir)
            pfqc.wait()
            qcpass, qtrim, atrim, recheck = get_qc(fqcdir+'2ndpass',
                                                           passthrough, qcconf)

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
    description = ("This script qcconf FastQC output for PASS/WARN/FAIL values")
    args = sqcu.parse_command_line(description)

    args = sqcu.make_paths(args)
    args.files = sqcu.get_files(args)
    args.qcconf = sqcu.get_qcconfig(args.config)

    ### Check FastQC output, simple yes/no to quality trimming
    ### Output and resubmission of jobs handled by checkFastQC
    check_qc(args.files, args.fqcdir, args.trimdir, args.tmpdir, args.adaptseq,
                args.qcconf)
