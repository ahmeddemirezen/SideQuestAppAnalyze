from selenium import webdriver
import time
from bs4 import BeautifulSoup
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


driver = webdriver.Edge(EdgeChromiumDriverManager().install())

df = pd.read_csv('sidequest.csv', index_col=0)

print(df.head())

df['click'] = ''
df['view'] = ''

print(df.head())

totalCount = df['url'].count()
printProgressBar(0, totalCount, prefix='Progress:',
                 suffix='Complete', length=50)
for index in range(totalCount):
    printProgressBar(index + 1, totalCount, prefix='Progress:',
                     suffix='Complete', length=50)
    try:
        driver.get(df['url'][index])
        time.sleep(0.1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        card = soup.find(
            'div', attrs={'class': 'row right-section center-align stats-padding'})
        df.at[index, 'click'] = card.find(
            'div', attrs={'class': 'counter download-counter-box'}).text
        df.at[index, 'view'] = card.find_all(
            'div', attrs={'class': 'counter'})[2].text
    except:
        continue

driver.quit()

print(df.head())

df.to_csv('sidequest_click_view.csv')
