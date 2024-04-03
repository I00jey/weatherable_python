import requests
from bs4 import BeautifulSoup as bs
from Crawling.seleniumCrawling import get_clothes_detail_info
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

# mongoDB 연결
mongodb_URL = os.getenv("MONGODB_URL")
client = MongoClient(mongodb_URL)
db = client.weatherable
clothes = db.clothes


def get_clothes_list(shopping_mall_url):
    response = requests.get(shopping_mall_url)
    response.raise_for_status()
    soup = bs(response.content, 'html.parser')
    element_array = soup.select('#searchList > li:nth-child(n) > div.li_inner')
    product_data_list = []
    for index, element in enumerate(element_array, start=1):
        try:
            small_img_element = element.select_one("div.li_inner > div.list_img > a > img")
            small_img = small_img_element['data-original'] if small_img_element else None
            a_find = element.select_one("div.li_inner > div.list_img > a")
            path = a_find['href'] if a_find else None
            url = f"https:{path}" if path else None
            brand = element.select_one("div.li_inner > div.article_info > p.item_title > a").get_text(strip=True)
            product_name = element.select_one("div.li_inner > div.article_info > p.list_info > a")['title']

            # 제품 상세정보 수집
            clothes_detail_info = get_clothes_detail_info(url)
            big_img = clothes_detail_info['big_img']
            thickness = clothes_detail_info['thickness']
            season = clothes_detail_info['season']
            size = clothes_detail_info['size']
            price = clothes_detail_info['price']

            data = {"major_category": "Outer",
                    "middle_category": "Padded_jacket",
                    "price": price,
                    "thickness": thickness,
                    "product_name": product_name,
                    "brand": brand,
                    "small_img": small_img,
                    "big_img": big_img,
                    "size": size,
                    "season": season}

            try:
                # insert_one(document) : Document 추가
                insert_result_id = clothes.insert_one(data).inserted_id
                if insert_result_id:
                    print(str(index) + '번째 저장 성공')

            except Exception as e:
                print(f"Error: {e}")
                print(f"Failed to insert data into MongoDB for product {index}. Moving to the next product.")
                continue

        except Exception as e:
            print(f"Error: {e}")
            print("Failed to extract data from the current element. Moving to the next element.")
            continue


for i in range(9, 10):
    print(f"{i}번째 페이지")
    product_list_url = f"https://www.musinsa.com/categories/item/002013?d_cat_cd=002013&brand=&list_kind=small&sort=pop_category&sub_sort=&page={i}&display_cnt=90&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure="
    get_clothes_list(product_list_url)
