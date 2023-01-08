import datetime
import os
import subprocess
import pandas


def main():
    """
    Main - program execute
    Fixes the seqName column in nextclade output. For output sourced from GISAID's "All sequences" FASTA file (output as sequences.tsv), the format is different. 
    Lookup the consistent value using the metadata.tsv file (from GISAID), assuming that is at least as up-to-date and your sequences.tsv file
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    datadir = 'C:/Dev/nextclade/'
    filename_metadata = 'C:/Dev/sars-cov-2-genomes/metadata.tsv'
    needed_columns_metadata = ['Virus name', 'Accession ID', 'Collection date', 'Submission date']

    print (str(datetime.datetime.now()) + ' Reading and deriving columns from: ' + filename_metadata)
    df_metadata_in = pandas.read_csv(filename_metadata, usecols = needed_columns_metadata, sep="\t")
    df_metadata_in['seqName new'] = df_metadata_in['Virus name'] + '|' + df_metadata_in["Accession ID"] + '|' + df_metadata_in["Collection date"]
    df_metadata_in['seqName VCS'] = df_metadata_in['Virus name'] + '|' + df_metadata_in["Collection date"] + '|' + df_metadata_in["Submission date"]
    df_metadata = df_metadata_in[['seqName new', 'seqName VCS']]
    print(df_metadata.head(10))

    filename_sequences = datadir + 'output/sequences.tsv'
    needed_columns_sequences = ['seqName', 'clade', 'Nextclade_pango', 'partiallyAliased']

    print (str(datetime.datetime.now()) + ' Updating: ' + filename_sequences)
    df_sequences = pandas.read_csv(filename_sequences, usecols = needed_columns_sequences, sep="\t")
    df_sequences = df_sequences.rename(columns={'seqName': 'seqName old'})
    print(df_sequences.head(10))
    df_sequences_out = df_sequences.merge(df_metadata, left_on=df_sequences['seqName old'].str.lower(), right_on=df_metadata['seqName VCS'].str.lower(), how='left')

    df_sequences_out['seqName'] = df_sequences_out['seqName new'].combine_first(df_sequences_out['seqName old'])
    df_sequences_out.to_csv(filename_sequences, columns = needed_columns_sequences, index=False, sep="\t" )

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()