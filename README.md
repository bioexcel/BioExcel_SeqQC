# SeqQC

TO BE UPDATED SOON.

Python scripts for a Sequence Quality Control pipeline, based on workflows
defined by IGMM.

Each tool can be run standalone, or as a whole workflow.

Requirements:

- FastQC
- Cutadapt
- Python (only tested with 2.7.10/13)

Above packages can be easily obtained via installing BCBio, which also includes packages used in further downstream analysis. - Make sure paths are correctly set up if done so.

## Future plans

- Provide CWL-compliant examples and tool-descriptors for basic usage (cannot do loops within CWL so must still use Python as workflow management, but CWL runners could run whole scripts/workflow with correct tool descriptions)
- Create Singularity container of workflow
- Make it easier for user to configure logic behind PASS/WARN/FAIL flags from FastQC
