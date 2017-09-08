# SeqQC
Python scripts for submitting Sequence Quality Control pipeline to PBS-based machines (e.g. Cirrus)

Other scripts can also be used within other workflows and pipelines, or run as standalone tools (only possible with SeqQC.py script for now)

Requirements:
- FastQC
- Cutadapt
- Python (only tested with 2.7.10/13)

Above packages can be easily obtained via installing BCBio, which also includes packages used in further downstream analysis.
- Make sure paths are correctly set up if done so.

## Future plans

- Make SeqQc installable as python module into current environment
- Make all modules/stages run as standalone programs
- Implement objects for easier control?
- Use [Compound Field Names](https://www.python.org/dev/peps/pep-3101/#simple-and-compound-field-names) to help with setting string values, especially in helping improve portability of job templates to non-PBS systems.
- Provide CWL-compliant examples and tool-descriptors for basic usage (cannot do loops within CWL so must still use Python as workflow management, but CWL runners could run whole scripts/workflow with correct tool descriptions)