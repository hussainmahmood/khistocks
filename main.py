import os
import time
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import pandas as pd

def read_and_write_table(symbol, table, table_type):
    if not os.path.exists(f"data/{symbol}"):
        os.makedirs(f"data/{symbol}")

    header = []
    df_arr = []
    isHeader = True
    
    pret = bs(table.get_attribute('innerHTML'), features='lxml') 
    for tr in pret.find_all('tr'):
        if isHeader:
            isHeader = False
            for th in tr.find_all("th"):
                header.append(th.get_text().strip())
        else:
            temp_arr = []
            for td in tr.find_all("td"):
                temp_arr.append(td.get_text().strip())
            df_arr.append(temp_arr)

    df = pd.DataFrame(data=df_arr, columns=header)
    df.to_csv(f'data/{symbol}/{table_type}.txt', index=False)


def main():
    opt = wd.ChromeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--remote-debugging-port=9222')
    opt.add_argument('--incognito')
    opt.add_argument('--ignore-certificate-errors')
    drv = wd.Chrome('../chromedriver_win32/chromedriver' , options=opt)
    table_types = ['ratio', 'balance_sheet', 'income_statement', 'cash_flow', 'equity']
    symbols = pd.read_excel('pak_stock_symbol.xlsx', header=0, squeeze=True)
    for symbol in symbols:
        print(symbol)
        drv.get(f'https://www.khistocks.com/company-information/financial-highlights/{symbol}.html')
        for table_type in table_types:
            try:
                drv.find_element_by_css_selector(f"option[value={table_type}]").click()
                time.sleep(1)
                table = drv.find_element_by_id('f_table')
                read_and_write_table(symbol, table, table_type)
            except:
                pass

    drv.quit()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")
