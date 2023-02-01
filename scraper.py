from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter
from datetime import datetime

#print('Input the url link you want to scrape')
#url = input('>')

#url = 'https://www.trustpilot.com/review/nestle.de'
url = 'https://www.trustpilot.com/review/www.danskebank.dk'
#url = 'https://www.trustpilot.com/review/www.att.com'
#url = 'https://www.trustpilot.com/review/dior-us.com'
#url = 'https://www.trustpilot.com/review/uspoloassn.com'
workbook =''
page_count = 1
row_id = 0

def create_file(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    company_name = soup.find('span', class_ = 'typography_display-s__qOjh6 typography_appearance-default__AAY17 title_displayName__TtDDM').text
    workbook = xlsxwriter.Workbook(f'files/{company_name}.xlsx')
    workbook.close()
    print(company_name)

def get_data(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    return soup

def get_next_page(soup):
    page = soup.find('nav', class_ = 'pagination_pagination___F1qS')
    if not page.find('a', class_ = 'link_internal__7XN06 link_disabled__mIxH1 button_button__T34Lr button_l__mm_bi button_appearance-outline__vYcdF button_squared__21GoE link_button___108l pagination-link_disabled__7qfis pagination-link_next__SDNU4 pagination-link_rel__VElFy'):
        url = 'https://www.trustpilot.com' + str(page.find('a', class_ = 'link_internal__7XN06 button_button__T34Lr button_l__mm_bi button_appearance-outline__vYcdF button_squared__21GoE link_button___108l pagination-link_next__SDNU4 pagination-link_rel__VElFy')['href'])
        return(url)
    else:
        return

def find_reviews(soup):
    data =[]
    global row_id
    reviews = soup.find_all('div', class_ ='styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ')
    company_name = soup.find('span', class_ = 'typography_display-s__qOjh6 typography_appearance-default__AAY17 title_displayName__TtDDM').text


    for index, review in enumerate(reviews):
        item = {}
        item['Id'] = row_id
        item['Company Name'] = company_name
        item['Reviewer Name'] = review.find('span', class_ = 'typography_heading-xxs__QKBS8 typography_appearance-default__AAY17').text
        item['Reviewer Location'] = review.find('div', class_ = 'typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua').span.text
        item['Stars Given'] = int(review.find('div', class_ ='star-rating_starRating__4rrcf star-rating_medium__iN6Ty').img['alt'].split()[1])
        item['Review Heading'] = review.find('h2', class_ = 'typography_heading-s__f7029 typography_appearance-default__AAY17').text
        try:
            item['Review Text'] = review.find('p', class_ = 'typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn').text
        except:
            item['Review Text'] = "No data found"

        date_string = review.find('p', class_ = 'typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_color-black__5LYEn').text.split(':')[1]
        item['Date of Review'] = datetime.strptime(date_string, ' %B %d, %Y').date()

        data.append(item)
        row_id += 1
    return data


def export_data(data):
    df = pd.DataFrame(data)
    global page_count

    if page_count == 1:
        with pd.ExcelWriter(f'files/{df.iloc[:,1][0]}.xlsx',mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name="Sheet1",index=False)
        page_count = page_count + 1
    else:
        with pd.ExcelWriter(f'files/{df.iloc[:,1][0]}.xlsx',mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name="Sheet1",header=None, startrow=writer.sheets["Sheet1"].max_row,index=False)


create_file(url)
while True:
    soup = get_data(url)
    data = find_reviews(soup)
    export_data(data)
    url = get_next_page(soup)
    if not url:
        break
    print(url)

print("Done")
