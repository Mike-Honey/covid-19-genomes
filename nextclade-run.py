import datetime
import os
import subprocess
import pandas


def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    datadir = 'C:/Dev/nextclade/'
    nextclade_cmd_template = 'nextclade run --input-dataset ' + \
        datadir + 'data\sars-cov-2 -q --output-tsv=' + \
        datadir + 'output\[filename].tsv ' + \
        datadir + 'input\[filename].fasta'
    needed_columns = ['seqName', 'clade', 'Nextclade_pango', 'partiallyAliased']

    for file in os.listdir(datadir + 'input'):
        filename = os.fsdecode(file)
        # process each input .fasta file, only if a matching output .tsv file does not exist.
        if filename.endswith('.fasta') and not os.path.exists(str.replace(datadir + 'output/' + filename, ".fasta", ".tsv")):
            nextclade_cmd = str.replace(nextclade_cmd_template, "[filename]", str.replace(filename,".fasta", ""))
            print (str(datetime.datetime.now()) + ' Calling: ' + nextclade_cmd)
            subprocess.call (nextclade_cmd, shell=True)
            
            filename_tsv = str.replace(filename,".fasta", ".tsv")
            print (str(datetime.datetime.now()) + ' Dropping columns from: ' + filename_tsv)
            df1 = pandas.read_csv(datadir + "output/" + filename_tsv, usecols = needed_columns, sep="\t")
            df1.to_csv(datadir + "output/" + filename_tsv, index=False, sep="\t" )

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()