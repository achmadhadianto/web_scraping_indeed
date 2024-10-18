from curl_cffi import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd

url = 'https://www.indeed.com/jobs?'  # ternyata dari sini search bisa gagal
site = 'https://www.indeed.com'

params = {
    'q': 'Data Science',
    'l': 'New York, NY',
    #'start': ''  #perpage nambah 10
    #'pp' : #beda semua, ngga bisa dijadikan parameter
}

resp = requests.get(url, params=params, impersonate="chrome")
print(resp.status_code)

def get_total_pages():
    params = {
        'q': 'Data Science',
        'l': 'New York, NY',
        # 'start': ''  #perpage nambah 10
        # 'pp' : #beda semua, ngga bisa dijadikan parameter
    }

    resp = requests.get(url, params=params, impersonate="chrome")

    try:
        os.mkdir('temp')  # membuat folder temp
    except FileExistsError:
        pass

    with open('temp/resp.html', 'w+') as outfile:  # membuat file index.html di folder temp
        outfile.write(resp.text)
        outfile.close()

    total_pages = []
    # Scraping Step
    soup = BeautifulSoup(resp.text, 'html.parser')
    pagination = soup.find('ul', 'css-1g90gv6 eu4oa1w0') #mesti di teliti ulang
    pages = pagination.find_all('li') #mesti di teliti ulang
    for page in pages:
        total_pages.append(page.text)

    total = int(max(total_pages))
    return total

def get_all_items(): #parameter yang bisa di ubah-ubah query, location, start

    params = {
        'q': 'Data Science',
        'l': 'New York, NY',
        # 'start': ''  #perpage nambah 10
        # 'pp' : #beda semua, ngga bisa dijadikan parameter
    }

    resp = requests.get(url, params=params, impersonate="chrome")

    try:
        os.mkdir('temp')  # membuat folder temp
    except FileExistsError:
        pass

    with open('temp/resp.html', 'w+') as outfile:  # membuat file index.html di folder temp
        outfile.write(resp.text)
        outfile.close()

    soup = BeautifulSoup(resp.text, 'html.parser')
    #print(soup.prettify()) #dari 200 hal

    contents = soup.find_all('table',
                             'big6_visualChanges')  # cari yang mencangkup semua, nah bener pas diatas li yang banyak
    #print(contents) #jadi 26 hal #semua ini ternyata karena kita harus input table, bukan list html

    jobs_list = []
    for item in contents:
        job_title = item.find('h2', 'jobTitle').text  # bisa juga ternyata, coba gabung deh
        #print(job_title)
        company_name = item.find('div', 'css-1qv0295').text #kalau div ternyata bisa pakai text
        #print(company_name)
        company_location = item.find('div', 'css-1p0sjhy eu4oa1w0').text
        #print(company_location)
        link = item.find('a', 'jcs-JobTitle')
        try:
            job_link = site + link.get('href')
        except:
            job_link = 'link is not availavble'
        #print(job_link)

        #sorting data
        data_dict = { #mirip json
            'title' : job_title,
            'company' : company_name,
            'location' : company_location,
            'link' : job_link
        }
        #print(data_dict)

        jobs_list.append(data_dict)

    #sama saja
    print('Jumlah Datanya Adalah', len(jobs_list))
    #print(f'jumlah data: {len(jobs_list)}')
    print(jobs_list)

    #writing json file
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    with open('json_result/{query}_in_{location}_page_{page}.json', 'w+') as json_data: #w+ ngaruh enter
        json.dump(jobs_list, json_data)
    print('json created')

def create_document(dataFrame, filename):
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass

    df = pd.DataFrame(dataFrame)
    df.to_csv(f'data_result/{filename}.csv', index=False)
    df.to_excel(f'data_result/{filename}.xlsx', index=False)

    print(f'File {filename}.csv and {filename}.xlsx successfully created')

def run():
    query = input('Enter your query: ')
    location = input('Enter your location: ')

    total = get_total_pages(query, location)
    counter = 0
    final_result = []
    for page in range(total):
        page += 1
        counter += 10
        final_result += get_all_items(query, location, counter, page)

    #formating data
    try:
        os.mkdir('reports')
    except FileExistsError:
        pass

    with open('reports/{}.json'.format(query), 'w+') as final_data:
        json.dump(final_result, final_data)

    print('Data Json Ceated')

    #create document
    create_document(final_result, query) #dataFrame, filename

if __name__ == '__main__':
    run()
