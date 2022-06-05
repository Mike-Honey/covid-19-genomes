import datetime
import numpy
import os
import pandas
import requests
from bs4 import BeautifulSoup
from io import StringIO

def processWebPageTables(webpageURL, datadir, filename, table_instance, check_diff, sort_rows):

    html_page_df = pandas.read_html(webpageURL)
    html_table_df = html_page_df[table_instance]
    print ( html_table_df )

    # strip unicode characters
    html_table_cols = html_table_df.select_dtypes(include=[object]).columns.tolist()
    html_table_df[html_table_cols] = html_table_df[html_table_cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))
    if sort_rows:
        html_table_df = html_table_df.sort_values(by=html_table_cols)

    if check_diff:
        input_xlsx_df = pandas.read_excel(datadir + filename)
        # print ( input_xlsx_df )

        diff_df = pandas.merge(input_xlsx_df, html_table_df, how='outer', indicator='Exist')

        diff_df = diff_df.loc[diff_df['Exist'] != 'both']
        diff_df['Exist'] = diff_df['Exist'].replace('left_only', 'old')
        diff_df['Exist'] = diff_df['Exist'].replace('right_only', 'new')
        diff_df = diff_df.sort_values(by=diff_df.columns.tolist())
        diff_file_name = datadir + str.replace(filename, '.xlsx', '_diff.xlsx')
        if len(diff_df.index) > 0:
            print(str(datetime.datetime.now()) + ' Differences found, wrote to file: ' + diff_file_name )
            diff_df.to_excel (diff_file_name, index=False)

    # write current data to excel file for next comparison run, also to timestamped file.
    html_table_df.to_excel (datadir + filename, index=False)
    html_table_df.to_excel (datadir + 'archive/' + str.replace(filename, '.xlsx', '_' + datetime.datetime.now().strftime('%y-%m-%d_%H_%M_%S') + '.xlsx'), index=False)


def processWebPageText(webpageURL, datadir, filename):
    response = requests.get(webpageURL)
    soup = BeautifulSoup(response.text, 'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # find chunk of interest
    # chunk_oi = '\n'.join(chunk for chunk in chunks if str(chunk).startswith('Date data was last updated'))
    chunk_oi = '\n'.join(chunk for chunk in chunks if str(chunk).startswith('Table shows sequence data'))
    text = chunk_oi.split('Global')[0]

    print(str(datetime.datetime.now()) + ' Found update date:' + text)

    # write current data to excel file for next comparison run, also to timestamped file.
    update_date_data = StringIO("""update_date
        """ + text )
    update_date_df = pandas.read_csv(update_date_data, sep=";")
    update_date_df.to_excel (datadir + filename, index=False)
    update_date_df.to_excel (datadir + 'archive/' + str.replace(filename, '.xlsx', '_' + datetime.datetime.now().strftime('%y-%m-%d_%H_%M_%S') + '.xlsx'), index=False)


def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    webpageURL = 'https://www.cdgn.org.au/variants-of-concern'
    datadir = 'C:/Dev/covid-19-genomes/cdgn-variants-of-concern/'
    check_diff = False
    sort_rows = False

    filename = 'cdgn-variants-of-concern_0.xlsx'
    table_instance = 0
    processWebPageTables(webpageURL, datadir, filename, table_instance, check_diff, sort_rows)

    filename = 'cdgn-variants-of-concern_1.xlsx'
    table_instance = 1
    processWebPageTables(webpageURL, datadir, filename, table_instance, check_diff, sort_rows)

    filename = 'cdgn-variants-of-concern_update-date.xlsx'
    processWebPageText(webpageURL, datadir, filename)

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()
