# SeqQC
Python scripts for submitting Sequence Quality Control pipeline to PBS-based machines (e.g. Cirrus)

Other scripts can also be used within other workflows and pipelines, or run as standalone tools (only possible with SeqQC.py script for now)

Requirements:
- FastQC
- Cutadapt
- Python (only tested with 2.7.10/13)

Above packages can be easily obtained via installing BCBio, which also includes packages used in further downstream analysis.
- Make sure paths are correctly set up if done so.