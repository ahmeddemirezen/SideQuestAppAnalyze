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
iteration = 100
printProgressBar(0, iteration, prefix='Progress:',
                 suffix='Complete', length=50)
scroolVal = 300
for i in range(iteration):
    printProgressBar(i + 1, iteration, prefix='Progress:',
                 suffix='Complete', length=50)
    time.sleep(0.5)
    start = i * scroolVal
    end = (i + 1) * scroolVal
    driver.execute_script(f"window.scrollTo({start},{end})")

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

appNames = []
priceTypes = []
ratings = []
ratingsCount = []
urls = []

for card in soup.find_all('div', attrs={'class': 'z-depth-5 ng-star-inserted'}):
    bottomPanel = card.find('div', attrs={'class': 'app-name-text truncate'})
    priceType = bottomPanel.find(
        'div', attrs={'class': 'right light-grey-text small-text'})
    priceTypes.append(priceType.text)
    priceType.decompose()
    appNames.append(bottomPanel.text)

    imagePanel = card.find('div', attrs={
                           'class': 'listing-rating inline-block listing-left-badge z-depth-2 ng-star-inserted'})
    count = imagePanel.find('span', attrs={'class': 'rating-number'})
    ratingsCount.append(count.text)
    count.decompose()
    imagePanel.find('i', attrs={'class': 'sq-icon'}).decompose()
    ratings.append(imagePanel.text)

    url = card.find('a')['href']
    urls.append(url)


df = pd.DataFrame()

df['name'] = appNames
df['price_type'] = priceTypes
df['rating'] = ratings
df['rating_count'] = ratingsCount
df['url'] = urls

# data cleaning
df['name'] = df['name'].apply(lambda x: x.replace(' ', '').lower())
df['price_type'] = df['price_type'].apply(lambda x: x.lower())
df['rating'] = df['rating'].apply(lambda x: float(x))
df['rating_count'] = df['rating_count'].apply(
    lambda x: int(x.replace('(', '').replace(')', '')))
df['url'] = df['url'].apply(lambda x: 'https://sidequestvr.com' + x)

print(df.describe())
print(df.head())

df.to_csv('sidequest.csv', index=False)
