from multiprocessing import Pool
import csv
import argparse
import os
import subprocess

def select_repos(input_file):
    repos = []
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if 500 < int(row[1]) < 28000:
                line_count += 1
                repos.append(row[0])

        print('Selected ' + str(line_count) + ' repos to analyze:', repos)
    return repos


def run(repo, output_prefix, log_prefix):
    pid = os.getpid()
    output_file = os.getcwd() + os.sep + output_prefix + str(pid) + '.csv'
    log_file = os.getcwd() + os.sep + log_prefix + str(pid) + '.txt'

    print(f'Process {pid} started for project {repo}.\nSaving output in {output_file}.\nSaving log in {log_file}.')
    with open(log_file, "w") as out:
        subprocess.run(f'python3 merge_analysis.py --local {repo} --collect --output {output_file}',
                       shell=True, stdout=out, stderr=subprocess.STDOUT)
    print(f'Process {pid} finished.')

def main():
    parser = argparse.ArgumentParser(description='Merge effort analysis over multiple projects')
    parser.add_argument("--processes", type=int, default=os.cpu_count(), help="number of processes to run in parallel. Default: number of cpus")
    parser.add_argument("input", help="input CSV file containing the path and the number of merges of each repository")
    parser.add_argument("--output-prefix", default="output", help="output prefix of the CSV file to be generated, containing the collected metrics. Default: 'output'")
    parser.add_argument("--log-prefix", default="log", help="log file prefix. Default: 'log'")

    args = parser.parse_args()

    selected_repos = select_repos(args.input)

    pool = Pool(processes=args.processes, maxtasksperchild=1)
    for repo in selected_repos:
        pool.apply_async(run, args=(repo, args.output_prefix, args.log_prefix))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()