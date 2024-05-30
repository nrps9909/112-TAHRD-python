import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json

def fetch_setn_news():
    url = 'https://www.setn.com/ViewAll.aspx'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('h3', class_='view-li-title')
        
        news_data = []
        for article in articles[:20]:  # 抓取前20篇文章
            title_tag = article.find('a')
            if title_tag:
                title = title_tag.get_text().strip()
                link = title_tag['href']
                if not link.startswith('http'):
                    link = 'https://www.setn.com' + link
                
                article_response = requests.get(link)
                if article_response.status_code == 200:
                    article_soup = BeautifulSoup(article_response.content, 'html.parser')
                    paragraphs = article_soup.find_all('p')
                    content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                    content = clean_text(content)  # 清洗內容
                    news_data.append({'Title': title, 'Content': content})
                else:
                    print(f"Failed to fetch article content, status code: {article_response.status_code}")
            else:
                print("Title tag not found.")
        
        return news_data
    else:
        print(f"Failed to fetch SETN news, status code: {response.status_code}")
        return []

def clean_text(text):
    text = re.sub(r'\[.*?\]', '', text)  # 去除引用
    text = re.sub(r'\s+', ' ', text).strip()  # 去除多餘空白
    text = re.sub(r'針對目前國會的現況，請問您支持下列哪一種做法？', '', text)  # 去除特定重複內容
    return text

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    news_data = fetch_setn_news()
    
    if not news_data:
        print("No data fetched.")
        return
    
    cleaned_data = []
    for item in news_data:
        cleaned_content = clean_text(item['Content'])
        cleaned_data.append({'Title': item['Title'], 'Content': cleaned_content})
    
    # 結構化資料
    data_dict = [{"Title": item['Title'], "Content": item['Content']} for item in cleaned_data]
    
    # 保存資料到CSV和JSON檔
    csv_filename = "setn_news.csv"
    json_filename = "setn_news.json"
    save_to_csv(cleaned_data, csv_filename)
    save_to_json(data_dict, json_filename)
    
    print(f"Data saved to {csv_filename} and {json_filename}")

if __name__ == "__main__":
    main()
