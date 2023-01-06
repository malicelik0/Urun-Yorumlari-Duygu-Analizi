# encoding:utf-8
from encodings import utf_8
from requests_html import HTMLSession
import json
import time


class Rewiews:
    def __init__(self, asin) -> None:
        self.asin = asin
        self.session = HTMLSession()
        self.headers = {
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        self.url = f'https://www.amazon.com.tr/product-reviews/{self.asin}/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='

    def pagination(self, page):
        r = self.session.get(self.url + str(page))
        if not r.html.find('div[data-hook=review]'):
            return False
        else:
            return r.html.find('div[data-hook=review]')

    def parse(self, reviews):
        total = []
        for review in reviews:

            if review.find(
                    'i[data-hook=cmps-review-star-rating] span', first=True) == None:
                rating = ""
            else:
                rating = review.find(
                    'i[data-hook=cmps-review-star-rating] span', first=True).text

            if review.find(
                    'span[data-hook=review-body] span', first=True) == None:
                body = ""
            else:
                body = review.find(
                    'span[data-hook=review-body] span', first=True).text.replace('\n', '').strip()

            data = {
                'rating': rating,
                'body': body
            }
            total.append(data)
        return total

    def save(self, results):
        with open('B07YDH98RB1.json', 'a', encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)


if __name__ == '__main__':
    amz = Rewiews('B07YJHXZT6')
    results = []
    for x in range(30, 500):
        time.sleep(1)
        reviews = amz.pagination(x)
        if reviews is not False:
            results.append(amz.parse(reviews))
        else:
            print('no more pages')

        print(results)
        print(x)
    amz.save(results)
