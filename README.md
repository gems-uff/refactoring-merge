# Refactoring and Merge Effort

This project aims to analyze the relationship between the occurrence of refactorings and the merge effort.

## Getting Started

### Prerequisites

This project requires python, pygit2, libgit2, mysql and RefactoringMiner, and it was tested on the following versions:

```
python==3.6
pygit2==0.27.0
libgit2==0.27.0
mysql==8.0.23
RefactoringMiner==2.1
```

### Preparing the runtime environment:

#### Install libgit2/pygit2

First of all, if you are using Mac OS or Linux you need to install libgit2. If you have Anaconda installed in your computer, you can simple do:

```
$ conda install -c conda-forge libgit2
```

Otherwise, on Mac OS you can install libgit2 using homebrew:

```
$ brew install libgit2
```

On Linux you can install the latest version of libgit2 by doing:

```
$ wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz
$ tar xzf v0.27.0.tar.gz
$ cd libgit2-0.27.0/
$ cmake .
$ make
$ sudo make install
$ sudo ldconfig
```

For more information http://www.pygit2.org/install.html

#### Install mysql

1. Open the terminal and run the following command:

```
sudo apt update
```

2. Enter your password and wait for the update to finish.

3. Next, run:

```
sudo apt upgrade
```
4. Install

```
sudo apt install mysql-server
```

#### Install RefactoringMiner

We are using version 2.1 of RefactoringMiner. More details about the tool and installation steps can be found at: https://github.com/tsantalis/RefactoringMiner.

#### Clone Refactoring-Merge Project

URL: https://github.com/gems-uff/refactoring-merge.git.


#### Create the Database

The script for creating the database in mysql can be found in the file "script_database.sql" in the output folder of this project.


## Basic Usage

### Mining repositories on GitHub

To mine repositories on GitHub run the following script:

```
./mining_refactoring_merge.py --repo_path [local_path_git_project] --refminer_path [local_path_refminer] --merge_effort

```

Options:

--merge_effort = optional boolean parameter indicating whether the merge effort should be computed.

--repo_path = local path to where the Git project repository was cloned.

--refminer_path = local path where RefactoringMiner was installed.

--log = optional boolean parameter indicating to print the execution log.

### Building the Dataset

To build the dataset for the application of the data mining technique (extraction of association rules) just run the script "extract_merge_commits_score.py":

```
./extract_merge_commits_score.py --branches --selected_refactorings --datasetname ['datasetname.csv']

```

Options:

--branches  = Boolean that indicate to split refactoring attributes in two branches (b1 and b1). When not informed, the script will sum the total of refactorings of each type in the two branches.

--selected_refactorings = Boolean that indicate to compute only selected refactorings. When informed, the script will only consider the 33 types of refactorings considered in this study.

--datasetname = Name of the produced dataset. When not informed, the script will save in the "output" folder a csv file with the following name: "merge_refactoring_ds.csv"

## Team

Hidden due to ICSE submission.
<!-- * André Oliveira (UFF, Brazil)
* Leonardo Murta (UFF, Brazil)
* Alexandre Plastino (UFF, Brazil)
* Vânia Neves (UFF-Brasil)
* Ana Carla Bibiano (PUC-Rio)
* Alessandro Garcia (PUC-Rio) -->

<!-- ## Publications

* [MOURA, T.; MURTA, L. Uma técnica para a quantificação do esforço de merge. . In: VI WORKSHOP ON SOFTWARE VISUALIZATION, EVOLUTION AND MAINTENANCE. 2018](https://github.com/gems-uff/merge-effort/blob/master/docs/VEM_2018.pdf) -->

## License

Copyright (c) 2018 Universidade Federal Fluminense (UFF)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
