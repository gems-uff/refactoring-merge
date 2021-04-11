
import csv
import argparse

def get_merges_analyzed(input_file):
    merges_analyzed = {}
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            #print(row[-1])
            if(line_count != 0):

                if(row[-1] in merges_analyzed):
                    merges_analyzed[row[-1]] = merges_analyzed[row[-1]] + 1
                else:
                    print(row[-1])
                    merges_analyzed[row[-1]] = 1
            line_count += 1

        print('Processed ' + str(line_count))

    return merges_analyzed


def main():
    parser = argparse.ArgumentParser(description='Merge effort analysis over multiple projects')
    parser.add_argument("input", help="input CSV file containing the path and the number of merges of each repository")

    args = parser.parse_args()

    merges_analyzed = get_merges_analyzed(args.input)

    #print(merges_analyzed)
    print(len(merges_analyzed))


if __name__ == '__main__':
    main()