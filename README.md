# BioExcel_SeqQC

Python package to run a Sequence Quality Control pipeline, based on workflows
defined by IGMM.

## Requirements:

- FastQC
- Cutadapt
- Python 3.x
- Pyyaml

We recommend using the conda package manager, and making use of virtual 
environments. This tool also exists in the bioconda channel. This has the 
benefit of automatically installing all pre-requisites when installing this 
tool.

## Installation

There are two main ways to install the package.

### Conda package installation

#### Set up a new conda environment (optional):

```bash
$ conda create -n my_env -c bioconda python=3 
```

This creates a clean Python3 environment in which to install and run the tool. 
If you have a conda environment you already wish to use, make sure you add the 
bioconda channel to the environment, or your conda package as a whole.

#### Install BioExcel_SeqQC
```bash
$ conda install bioexcel_seqqc
```

This one line will install BioExcel_SeqQC and all of it's dependencies.

### Manual installation

If you wish to install manually, follow the steps below. We still recommend 
using some kind of virtual environment. Before running the workflow, install
the pre-requisite tools and ensure they are contained in your $PATH

```bash
$ git clone https://github.com/bioexcel/BioExcel_SeqQC.git
$ cd BioExcel_SeqQC
$ python setup.py install
```

## Usage

Once installed, there are several ways to use the tool. The easiest is to call
the executable script, which runs the whole workflow based on several options 
and arguments the user can modify. Find these using

```bash
$ bioexcel_seqqc -h
```

An example of basic usage of the pipeline is:

```bash
$ bioexcel_seqqc --files in1.fa in2.fa --threads 4 --outdir ./output
```

### Editing configuration for checkFastQC stage

The tool runs an automated set of checks based on output from FastQC. The 
default decision making is based on our partner preference, but these can be
changed. First, output an example configuration file (which contains the
default values):

```bash
$ bioexcel_seqqc --printconfig
```

The file lists the summary outputs from FastQC, and what decisions to make 
depending on whether the files should be trimmed, rechecked, and take into
account whether they have been trimmed automatically.

### Python Module

In addition to the executable version, the tool is installed as a Python 
package, so each stage can be imported as a module into other scripts, if the 
user wishes to perform more unique/complicated/expanded workflows. Each function
creates and returns a python subprocess.

```python
import bioexcel_seqqc
import bioexcel_seqqc.runfastqc as rfq
import bioexcel_seqqc.runtrim as rt

# Do things before running FastQC

fqc_process = rfq.run_fqc(infiles, fqcdir, tmpdir, threads)
fqc.wait()

# Do things after FastQC, and before trimming low quality reads

trim_process = rt.trimQC(infiles, trimdir, threads):
trim_process.wait()
```