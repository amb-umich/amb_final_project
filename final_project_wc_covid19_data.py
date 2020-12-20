#################################
##### Name: Ali M. Berri
##### Uniqname: aliberri
#################################

from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.request import urlretrieve as retrieve
import plotly.graph_objects as go
import sqlite3
import openpyxl

CACHE_FILENAME = "wc_covid19_data_cache.json"
BASE_URL = "https://www.michigan.gov"

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def get_covid_excel_data_url():
    '''Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''
    response = requests.get('https://www.michigan.gov/coronavirus/0,9753,7-406-98163_98173---,00.html')
    soup = BeautifulSoup(response.text, 'html.parser')
    mi_excel_parent = soup.find('div', id='comp_115341')
    mi_excel_name_tag = mi_excel_parent.find('span', class_='shortdesc')
    mi_excel_p = mi_excel_name_tag.find_all('p')
    #excel_file_name = []
    excel_file_url = []
    for p in mi_excel_p:
            #mi_excel_title = p.get_text()
            #excel_file_name.append(mi_excel_title)
            mi_excel_a = p.find('a')
            try:
                    mi_excel_path = mi_excel_a['href']
                    excel_file_url.append(f'{BASE_URL}{mi_excel_path}')
                    #print(mi_excel_path)
            except:
                    pass
    #excel_file_name.pop(0)
    #print(excel_file_name)
    return excel_file_url[1]

def download_and_save_data(url, filename_response):
    retrieve(url, filename_response+'.xlsx')

def convert_xlsx2db(filename_response):
    #datafile = filename_response
    con=sqlite3.connect(filename_response+".db")
    #cur=con.cursor()
    wb=pd.read_excel(filename_response+'.xlsx', sheet_name='Data', engine='openpyxl')
    wb.to_sql(filename_response, con=con, if_exists="replace")
    con.close()

def process_command(filename_response):
    graph_choice = input("\nSelect the type of graph to display by entering the corresponding number:\n\n(1) Cumulative Confirmed Deaths\n(2) Cumulative Confirmed Cases\n(3) Daily Confirmed Cases\n(4) Daily Probable Cases\n(5) Daily Confirmed Deaths\n(6) Daily Probable Deaths\n\nEnter Number:")
    filename_response = filename_response
    com_result = []
    conn = sqlite3.connect(filename_response+'.db')
    cur = conn.cursor()
    acceptable = ['1', '2', '3', '4', '5', '6']

    if graph_choice == '1':
        #this if statement is for 'cumulative confirmed death'
        cur.execute(f"SELECT County, CASE_STATUS, Date, \"Deaths.Cumulative\" from {filename_response} WHERE COUNTY = \"Wayne\" and CASE_STATUS = \"Confirmed\"")
        for row in cur:
            com_result.append(row)

        xval = []
        yval=[]

        for entry in com_result:
            xval.append(entry[2])
            yval.append(entry[3])

        bar_data = go.Bar(x=xval, y=yval)
        graph_title = go.Layout(title="Out-Wayne County COVID-19 Total Confirmed Deaths")
        fig = go.Figure(data=bar_data, layout=graph_title)
        fig.update_layout(title_x=.5)
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Deaths")
        fig.update_layout(title_font_size=30, title_font_color="Blue")
        fig.update_xaxes(title_font_size=15, title_font_color="Blue")
        fig.update_yaxes(title_font_size=15, title_font_color="Blue")
        fig.show()

    if graph_choice == '2':
        #this if statment is for 'cumulative confirmed cases'
        cur.execute(f"SELECT County, CASE_STATUS, Date, \"Cases.Cumulative\" from {filename_response} WHERE COUNTY = \"Wayne\" and CASE_STATUS = \"Confirmed\"")
        for row in cur:
            com_result.append(row)

        xval = []
        yval=[]

        for entry in com_result:
            xval.append(entry[2])
            yval.append(entry[3])

        bar_data = go.Bar(x=xval, y=yval)
        graph_title = go.Layout(title="Out-Wayne County COVID-19 Total Confirmed Cases")
        fig = go.Figure(data=bar_data, layout=graph_title)
        fig.update_layout(title_x=.5)
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Cases")
        fig.update_layout(title_font_size=30, title_font_color="Blue")
        fig.update_xaxes(title_font_size=15, title_font_color="Blue")
        fig.update_yaxes(title_font_size=15, title_font_color="Blue")
        fig.show()

    if graph_choice == '3':
        #this if statement is for 'daily confirmed cases'
        cur.execute(f"SELECT County, CASE_STATUS, Date, Cases from {filename_response} WHERE COUNTY = \"Wayne\" and CASE_STATUS = \"Confirmed\"")
        for row in cur:
            com_result.append(row)

        xval = []
        yval=[]

        for entry in com_result:
            xval.append(entry[2])
            yval.append(entry[3])

        bar_data = go.Bar(x=xval, y=yval)
        graph_title = go.Layout(title="Out-Wayne County COVID-19 Daily Confirmed Cases")
        fig = go.Figure(data=bar_data, layout=graph_title)
        fig.update_layout(title_x=.5)
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Cases")
        fig.update_layout(title_font_size=30, title_font_color="Blue")
        fig.update_xaxes(title_font_size=15, title_font_color="Blue")
        fig.update_yaxes(title_font_size=15, title_font_color="Blue")
        fig.show()

    if graph_choice == '4':
        #this if statement is for 'daily probable cases'
        cur.execute(f"SELECT County, CASE_STATUS, Date, Cases from {filename_response} WHERE COUNTY = \"Wayne\" and CASE_STATUS = \"Probable\"")
        for row in cur:
            com_result.append(row)

        xval = []
        yval=[]

        for entry in com_result:
            xval.append(entry[2])
            yval.append(entry[3])

        bar_data = go.Bar(x=xval, y=yval)
        graph_title = go.Layout(title="Out-Wayne County COVID-19 Daily Probable Cases")
        fig = go.Figure(data=bar_data, layout=graph_title)
        fig.update_layout(title_x=.5)
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Cases")
        fig.update_layout(title_font_size=30, title_font_color="Blue")
        fig.update_xaxes(title_font_size=15, title_font_color="Blue")
        fig.update_yaxes(title_font_size=15, title_font_color="Blue")
        fig.show()

    if graph_choice == '5':
        #this if statement is for 'daily confirmed deaths'
        cur.execute(f"SELECT County, CASE_STATUS, Date, Deaths from {filename_response} WHERE COUNTY = \"Wayne\" and CASE_STATUS = \"Confirmed\"")
        for row in cur:
            com_result.append(row)

        xval = []
        yval=[]

        for entry in com_result:
            xval.append(entry[2])
            yval.append(entry[3])

        bar_data = go.Bar(x=xval, y=yval)
        graph_title = go.Layout(title="Out-Wayne County COVID-19 Daily Confirmed Deaths")
        fig = go.Figure(data=bar_data, layout=graph_title)
        fig.update_layout(title_x=.5)
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Deaths")
        fig.update_layout(title_font_size=30, title_font_color="Blue")
        fig.update_xaxes(title_font_size=15, title_font_color="Blue")
        fig.update_yaxes(title_font_size=15, title_font_color="Blue")
        fig.show()

    if graph_choice == '6':
        #this if statement is for 'daily probable deaths'
        cur.execute(f"SELECT County, CASE_STATUS, Date, Deaths from {filename_response} WHERE COUNTY = \"Wayne\" and CASE_STATUS = \"Probable\"")
        for row in cur:
            com_result.append(row)

        xval = []
        yval=[]

        for entry in com_result:
            xval.append(entry[2])
            yval.append(entry[3])

        bar_data = go.Bar(x=xval, y=yval)
        graph_title = go.Layout(title="Out-Wayne County COVID-19 Daily Probable Deaths")
        fig = go.Figure(data=bar_data, layout=graph_title)
        fig.update_layout(title_x=.5)
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Deaths")
        fig.update_layout(title_font_size=30, title_font_color="Blue")
        fig.update_xaxes(title_font_size=15, title_font_color="Blue")
        fig.update_yaxes(title_font_size=15, title_font_color="Blue")
        fig.show()

    if graph_choice == "exit":
        print('bye')
        b="bye"
        return b

    if graph_choice not in acceptable:
        print("\n\nInvalid response. Try again")


# if __name__ == "__main__":
#     welcome_statment = 'Welcome to the automated Wayne County COVID-19 Data Graph Generator!'
#     print(welcome_statment)
#     print("-"*len(welcome_statment))

#     filename_response = f"{input('What do you want to call the saved MI COVID19 data excel sheet? (no need to add extention at the end) ')}"
#     get_covid_excel_data_url()

#     download_and_save_data(get_covid_excel_data_url(), filename_response)

if __name__ == "__main__":
    filename_response = f"{input('What do you want to call the saved MI COVID19 data excel sheet? (no need to add extention at the end) ')}"

    convert_xlsx2db(filename_response)

    while True:
        process_command(filename_response)
        if process_command(filename_response) == "bye":
            break


