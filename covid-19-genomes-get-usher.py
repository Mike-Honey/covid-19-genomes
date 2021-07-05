import datetime
import gzip
import shutil
import urllib.request


def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    webpageURL = 'http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2//public-latest.metadata.tsv.gz'
    filename = 'public-latest.metadata.tsv'
    datadir = 'C:/Dev/covid-19-genomes/usher/'
    
    # try:
    #     name, hdrs = urllib.request.urlretrieve(webpageURL, datadir + filename + '.gz')
    # except IOError as e:
    #     print ("Can't retrieve %r to %r: %s" % (webpageURL, datadir, e))
    #     return

    with urllib.request.urlopen(webpageURL) as response, open(datadir + filename + '.gz', 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    with gzip.open(datadir + filename + '.gz', 'rb') as f_in:
        with open(datadir + filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()
