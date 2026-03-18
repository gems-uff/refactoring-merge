# Refactoring and Merge Effort

This project aims to analyze the relationship between the occurrence of refactorings and the merge effort.

## Getting Started

### Prerequisites

This project requires Python, pygit2, libgit2, Mysql and RefactoringMiner, and it was tested on the following versions:

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

#### Install Mysql

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

Mining cloned repositories must be carried out in three steps: collecting branches, collecting code refactorings, and calculating the merge effort. The script that collects the branches must be the first to be executed. The other scripts are independent and can be executed in any order.

#### Script 1 - Collect Branches

```
./script_1_colllect_branches.py --database [data_base_name] --repo_path [local_repository_path]
```

Parameters:
```
--database = (mandatory) database name.
--repo_path = (mandatory) local path to where the Git project repository was cloned.
--log = (optional) boolean parameter indicating the need to print the execution log.
--retry (optional) boolean parameter indicating the need to retry the execution. This retry is only applicable when the repository is updated via git pull.
```

#### Script 2 - Collect Refactorings

```
./script_2_collect_refactorings.py --database [data_base_name] --repo_path [local_repository_path] --refminer_path [refminer_path] --arq_ref_miner [refminer_path_output_file] 
```

Parameters:
```
--database = (mandatory) database name.
--repo_path = (mandatory) local path to where the Git project repository was cloned.
--refminer_path = (mandatory) Refactoring Miner tool executable code path.
--arq_ref_miner = (mandatory) .json file name that will store the results returned by the Refactorings Miner tool.
--log = (optional) boolean parameter indicating the need to print the execution log.
--retry (optional) boolean parameter indicating the need to retry the execution. This new attempt is applicable in cases of interruptions in script execution or in Refactoring Miner timeout situations.
```

#### Script 3 - Calculate Merge Effort

```
./script_3_calculate_merge_effort.py --log --database [data_base_name] --repo_path [local_repository_path]
```

Parameters:
```
--database = (mandatory) database name.
--repo_path = (mandatory) local path to where the Git project repository was cloned.
--log = (optional) boolean parameter indicating the need to print the execution log.
--retry (optional) boolean parameter indicating the need to retry the execution. This new attempt is applicable in cases of interruptions in the execution of the script or in situations of timeout in the effort calculation.
```

**Merge Effort Computation**

The merge effort is computed by comparing the changes introduced in the merge commit with the changes performed independently in each branch, using a set-based formulation over code differences.

_Definitions_

Let:
- $C_{base}$: the common ancestor of the merge.
- $C_{merge}$: the merge commit.
- $C_{p1}, C_{p2}$: the parent commits of the merge.

_Calculations_

We compute the sets of actions as follows:

1. Actions introduced by the merge:
   - $$A_{merge} = \text{diff}(C_{base}, C_{merge})$$
  
2. Actions performed in each branch:
   - $$A_{b1} = \text{diff}(C_{base}, C_{p1})$$
   - $$A_{b2} = \text{diff}(C_{base}, C_{p2})$$

4. Total actions from both branches (union):
   - $$A_{branches} = A_{b1} \cup A_{b2}$$
     
6. Additional actions introduced during merge resolution:
   - $$A_{extra} = A_{merge} \setminus A_{branches}$$
     
_Final Metric_

The **Merge Effort** is defined as the cardinality (size) of the extra actions set:
   - $$\text{effort} = |A_{extra}|$$
  
_Note:_ 
This value represents the number of lines added or removed during the merge process that cannot be directly explained by the independent evolution of the branches—essentially measuring the manual work required to reconcile concurrent changes.

### Building the Dataset

To build the dataset for the application of the data mining technique (extraction of association rules) just run the script "extract_merge_commits_score.py":

```
./extract_merge_commits_score.py --branches --selected_refactorings --datasetname ['datasetname.csv']

```

Parameters:
```
--branches = (optional) boolean parameter indicating the need to split refactoring attributes into two branches (b1 and b2). When not informed, the script will sum the total of refactorings of each type in the two branches.
--selected_refactorings = (optional) boolean parameter indicating the need to compute only selected refactorings. When informed, the script will only consider the 33 types of refactorings considered in this study.
--datasetname = (optional) name of the produced dataset. When not informed, the script will save in the "output" folder a csv file with the following name: "merge_refactoring_ds.csv"

```

### Association Rule Extraction using Apriori Algorithm

In this stage, we implemented algorithms for extracting association rules using **Python** within the **Google Colab** environment. The process focuses on identifying co-occurrence patterns between sets of items.

#### Environment and Dependencies

To execute the scripts, the `apyori` library must be installed:

> [!IMPORTANT]
> Installation: `!pip install apyori`  
> Documentation: [PyPI - apyori](https://pypi.org/project/apyori/)

---

#### Google Colab Notebooks

You can access the full implementations through the following links:

* [Apriori Project - Part 1](https://colab.research.google.com/drive/1yK1aNFZqrTykgVKOYxD5FQvQSRK5jhy9?usp=drive_link)
* [Apriori Project - Part 2](https://colab.research.google.com/drive/1Pqu0AWviWlNkO11JFq_-hGAB6BF5E_kn?usp=drive_link)
* [Apriori Project - Part 3](https://colab.research.google.com/drive/1mz3OIu_I4e6oMp9ijTRtb4XhzLhDZHp0?usp=drive_link)

---

#### Evaluation Metrics

A rule $X \rightarrow Y$ indicates, with a certain assurance, that antecedent $X$ implies consequent $Y$. We evaluate rule relevance using three primary measures:

**1. Support**

Measures the percentage of instances in the dataset $D$ that satisfy both the antecedent and the consequent.

$$Sup_{(X \rightarrow Y)} = \frac{T_{X \cup Y}}{T}$$
*Where $T_{X \cup Y}$ is the number of records containing both $X$ and $Y$, and $T$ is the total number of records.*

**2. Confidence**

Measures the probability of the consequent occurring given the occurrence of the antecedent.
$$Conf_{(X \rightarrow Y)} = \frac{T_{X \cup Y}}{T_X}$$
*Where $T_X$ is the number of records satisfying the antecedent $X$.*

**3. Lift**

Shows how much more frequently $Y$ occurs when $X$ is present compared to its general occurrence. It is calculated by dividing the rule's Confidence by the Support of the consequent.
$$Lift_{(X \rightarrow Y)} = \frac{Conf_{(X \rightarrow Y)}}{Sup_{(Y)}}$$

_Lift Interpretation:_

* _Lift = 1:_ Indicates conditional independence; $X$ does not affect the occurrence of $Y$.
* _Lift > 1:_ Positive dependence ($X$ increases the probability of $Y$).
* _Lift < 1:_ Negative dependence ($X$ reduces the probability of $Y$).

> **Note:** Support and Confidence act as filters; only rules meeting the minimum input thresholds are extracted.


## Project corpus and dataset used in our latest study

Our latest study evaluated 64 open-source projects. The table below shows the characteristics of the projects selected for analysis, presenting the number of commits (**NC**), the number of merge commits (**NMC**), the number of merge commits using the *--no-ff* flag (**NMC-off**), and the number of valid merge commits (**NVMC**). The final version of the dataset discarded about 28.3% of the merges because they were generated by the Git command *--no-ff*, resulting in **91,270 merge commits**.

The study were conducted with **64 open-source projects** between **May 30, 2024**, and **June 1, 2024**.

This folder contains two compressed .csv files: **ds_os_join.csv** and **ds_os_split.csv** (available in this repository - folder *project-corpus*). Each dataset row represents a merge commit and its collected/calculated attributes. In the first one, the total number of refactorings for each type is added without considering the branch on which it was implemented. In the second one, these amounts are separated by branches.

#|Project Name|NC|NMC|NMC-nff|NVMC
| --- | ----------------- | ----- | --- | ------ | ---- |
|1|Activiti|11,696|1,920|682|1,238|
|2|aeron|17,074|957|157|800|
|3|android-oss|5,535|503|119|384|
|4|AntennaPod|8,858|2,323|725|1,598|
|5|antlr4|9,362|1,900|714|1,186|
|6|baritone|4,524|681|176|505|
|7|byte-buddy|7,521|356|117|239|
|8|camel|87,615|584|143|441|
|9|cas|42,344|5,619|764|4,855|
|10|closure-compiler|19,298|446|105|341|
|11|dbeaver|26,242|3,581|385|3,196|
|12|DependencyCheck|10,574|1,791|554|1,237|
|13|dolphinscheduler|9,878|1,351|353|998|
|14|dropwizard|11,363|1,342|620|722|
|15|druid|7,400|1,576|314|1,262|
|16|dubbo|8,913|694|8|686|
|17|elasticsearch|146,438|6,358|1,355|5,003|
|18|ExoPlayer|22,664|900|188|712|
|19|flink|47,108|653|29|624|
|20|FrameworkBenchmarks|14,566|2,507|514|1,993|
|21|ghidra|12,228|4,960|592|4,368|
|22|gocd|18,995|5,114|2,551|2,563|
|23|graphql-java|5,166|928|337|591|
|24|graylog2-server|30,003|1,979|324|1,655|
|25|hadoop|70,650|664|17|647|
|26|hibernate-orm|27,920|297|5|292|
|27|hive|22,158|334|8|326|
|28|incubator-druid|15,966|2,179|612|1,567|
|29|java-design-patterns|4,080|465|167|298|
|30|jenkins|35,612|5,091|660|4,431|
|31|jna|4237|696|351|345|
|32|k-9|15124|2,801|1,203|1,598|
|33|keycloak|25,850|4,858|1,856|3,002|
|34|languagetool|77,552|2,544|546|1,998|
|35|libgdx|15,367|2,738|601|2,137|
|36|lombok|3,756|357|55|302|
|37|metrics|5,206|498|209|289|
|38|micronaut-core|15,131|2,353|248|2,105|
|39|MinecraftForge|9,295|675|263|412|
|40|mockito|6,213|518|250|268|
|41|mybatis-3|5,259|1,296|757|539|
|42|mybatis-plus|5,981|709|180|529|
|43|nacos|5,413|1,131|342|789|
|44|NewPipe|11,226|2,196|572|1,624|
|45|okhttp|6,223|1,948|1,124|824|
|46|onedev|5,918|384|27|357|
|47|openapi-generator|23,499|2,911|739|2,172|
|48|OpenRefine|8,801|1,163|385|778|
|49|pentaho-kettle|30,304|6,742|2,720|4,022|
|50|pinpoint|14,677|1,968|999|969|
|51|realm-java|10,710|3,455|842|2,613|
|52|redisson|9,330|1,415|193|1,222|
|53|robolectric|14,758|3,910|1,240|2,670|
|54|RxJava|7,570|1,566|678|888|
|55|shardingsphere|42,603|2,793|658|2,135|
|56|skywalking|8,086|991|379|612|
|57|SmartTubeNext|9,736|1,829|780|1,049|
|58|smile|3,873|354|75|279|
|59|sonarqube|37,111|622|16|606|
|60|spring-framework|35,936|2,571|938|1,633|
|61|swagger-core|4,882|1,277|716|561|
|62|thingsboard|19,051|5,400|764|4,636|
|63|vert.x|11,504|1,413|403|1,010|
|64|zaproxy|9,544|3,121|1,582|1,539|
|-|**Totals**|**1,281,477**|**127,256**|**35,986**|**91,270**|

## Team

Hidden due to paper submission.

## License

Copyright (c) 2023 Universidade Federal Fluminense (UFF)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
