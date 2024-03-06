from requests import get, post
import cloudscraper
import time

def send_get_request(request_url, request_headers):
    response= get(request_url, headers=request_headers)
    return response.status_code, response

def send_post_request(request_url, post_data, request_headers):
    response= post(request_url, data=post_data, headers=request_headers)

    return response.status_code, response

def cloudscraper_request(request_url):
    cloudscraper_scraper= cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False })

    response= cloudscraper_scraper.get(request_url)
    return response.status_code, response