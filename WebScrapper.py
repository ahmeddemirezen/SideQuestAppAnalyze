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

driver.get('https://sidequestvr.com/apps/none/0/rating')

print("Web Scrapper Started")
iteration = 1000
printProgressBar(0, iteration, prefix='Progress:',
                 suffix='Complete', length=50)
scroolVal = 300
for i in range(iteration):
    printProgressBar(i + 1, iteration, prefix='Progress:',
                 suffix='Complete', length=50)
    time.sleep(0.01)
    start = i * scroolVal
    end = (i + 1) * scroolVal
    driver.execute_script(f"window.scrollTo({start},{end})")

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

df = pd.DataFrame()

df['name'] = ''
df['price_type'] = ''
df['rating'] = ''
df['rating_count'] = ''
df['url'] = ''

index = 0
for card in soup.find_all('div', attrs={'class': 'z-depth-5 ng-star-inserted'}):
    try:
        bottomPanel = card.find('div', attrs={'class': 'app-name-text truncate'})
        priceType = bottomPanel.find(
            'div', attrs={'class': 'right light-grey-text small-text'})
        df.at[index, 'price_type'] = priceType.text
        priceType.decompose()
        df.at[index, 'name'] = bottomPanel.text
    except:
        continue
    try:
        imagePanel = card.find('div', attrs={
                            'class': 'listing-rating inline-block listing-left-badge z-depth-2 ng-star-inserted'})
        count = imagePanel.find('span', attrs={'class': 'rating-number'})
        df.at[index, 'rating_count'] = count.text
        count.decompose()
    except:
        continue
    try:
        imagePanel.find('i', attrs={'class': 'sq-icon'}).decompose()
        df.at[index, 'rating'] = imagePanel.text
    except:
        continue
    try:
        url = card.find('a')['href']
        df.at[index, 'url'] = url
    except:
        continue
    index += 1
    




# data cleaning
df['name'] = df['name'].apply(lambda x: str(x).replace(' ', '').lower())
df['price_type'] = df['price_type'].apply(lambda x: str(x).lower())
df['rating'] = df['rating'].apply(lambda x: float(x))
df['rating_count'] = df['rating_count'].apply(
    lambda x: str(x).replace('(', '').replace(')', ''))
df['url'] = df['url'].apply(lambda x: 'https://sidequestvr.com' + str(x))

print(df.describe())
print(df.head())

df.to_csv('sidequest.csv', index=False)
