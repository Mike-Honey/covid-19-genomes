from collections import defaultdict
from dataclasses import replace
import datetime
import json
import pandas
import collections.abc


def flatten(dictionary, parent_key=False, separator='.', log=False):
    """
    Turn a nested dictionary into a flattened dictionary
    :param dictionary: The dictionary to flatten
    :param parent_key: The string to prepend to dictionary's keys
    :param separator: The string used to separate flattened keys
    :param log : Bool used to control logging to the terminal
    :return: A flattened dictionary
    """

    items = []
    for key, value in dictionary.items():
        if log: print('checking:',key)
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, collections.abc.MutableMapping):
            if log: print(new_key,': dict found')
            if not value.items():
                if log: print('Adding key-value pair:',new_key,None)
                items.append((new_key,None))
            else:
                items.extend(flatten(value, new_key, separator).items())
        elif isinstance(value, list):
            if log: print(new_key,': list found')
            if len(value):
                for k, v in enumerate(value):
                    items.extend(flatten({str(k): v}, new_key).items())
            else:
                if log: print('Adding key-value pair:',new_key,None)
                items.append((new_key,None))
        else:
            if log: print('Adding key-value pair:',new_key,value)
            items.append((new_key, value))
    return dict(items)



def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    filename = 'tree.json'
    datadir = 'C:/Dev/nextclade/data/sars-cov-2/'
    
    with open(datadir + filename, 'r') as fh:
            tree_dict = json.load(fh)

    # Flatten json to dict
    a = flatten(tree_dict["tree"])

    # Load to dataframe
    df = pandas.DataFrame.from_dict(a, orient='index', dtype=str)

    # Filter accordingly
    df = df[df.index.str.contains("node_attrs.Nextclade_pango|node_attrs.partiallyAliased")]

    print(df)

    df.to_csv(datadir + str.replace(filename,".json",".tsv"), sep='\t')

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()
