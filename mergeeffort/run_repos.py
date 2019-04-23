from multiprocessing import Pool
import csv
import argparse
import os
import subprocess

def select_repos(input_file, min_merges, max_merges):
    repos = []
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if min_merges <= int(row[1]) <= max_merges:
                line_count += 1
                repos.append(row[0])

        print('Selected ' + str(line_count) + ' repos to analyze:', repos)
    return repos


def run(repo, output_file, log_file):
    output_path = os.getcwd() + os.sep + output_file
    log_path = os.getcwd() + os.sep + log_file

    print(f'Starting project {repo}.\n\tOutput: {output_file}.\n\tLog: {log_file}.')
    with open(log_path, "w") as out:
        subprocess.run(f'python3 merge_analysis.py --local {repo} --collect --output {output_path}',
                       shell=True, stdout=out, stderr=subprocess.STDOUT)
    print(f'Finished project {repo}.')

def main():
    parser = argparse.ArgumentParser(description='Merge effort analysis over multiple projects')
    parser.add_argument("--processes", type=int, default=os.cpu_count(), help="number of processes to run in parallel. Default: number of cpus")
    parser.add_argument("--output-prefix", default="output-", help="output prefix of the CSV file to be generated, containing the collected metrics. Default: 'output-'")
    parser.add_argument("--log-prefix", default="log-", help="log file prefix. Default: 'log-'")
    parser.add_argument("--min-merges", type=int, default=500, help="the minimum number of merges to allow a project to be analized. Default: 500")
    parser.add_argument("--max-merges", type=int, default=28000, help="the maximum number of merges to allow a project to be analized. Default: 28000")
    parser.add_argument("input", help="input CSV file containing the path and the number of merges of each repository")

    args = parser.parse_args()

    selected_repos = select_repos(args.input, args.min_merges, args.max_merges)

    pool = Pool(processes=args.processes, maxtasksperchild=1)
    for i, repo in enumerate(selected_repos):
        pool.apply_async(run, args=(repo, args.output_prefix + str(i) + '.csv', args.log_prefix + str(i) + '.txt'))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()