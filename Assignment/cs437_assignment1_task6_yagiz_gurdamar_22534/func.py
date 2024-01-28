

import feedparser
from math import ceil
import json
import chardet
import re
import html
import logging

def decode_bytes(byte_data):
    detected = chardet.detect(byte_data)
    encoding = detected['encoding'] if detected['confidence'] > 0.5 else 'utf-8'

    try:
        decoded_data = byte_data.decode(encoding, errors='replace')
        return decoded_data, encoding
    except Exception as e:
        return None, str(e)


def extract_cdata(content):
    cdata_regex = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.DOTALL)
    matches = cdata_regex.findall(content)
    if matches:
        # CDATA içeriğini al ve HTML karakter referanslarını çözümle
        return html.unescape(matches[0])
    return content


def fetch_rss_feeds(rss_urls, keywords, articles_per_page=5):
    all_articles = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title, encoding = decode_bytes(entry.title.encode())
            summary, encoding = decode_bytes(entry.summary.encode())
            # Eğer başlık ve özet boş dönmüyorsa...
            if title and summary:
                # Başlığı ve özeti decode et
                entry.title = title
                entry.summary = summary
                # Bu makaleyi tüm makaleler listesine ekle (henüz filtreleme yapılmadı)
                all_articles.append(entry)

    # Anahtar kelimelere göre filtreleme
    filtered_articles = filter_articles_by_keywords(all_articles, keywords)

    # İlk 'articles_per_page' sayıda makaleyi döndür
    return filtered_articles[:articles_per_page]


def filter_articles_by_keywords(articles, keywords):
    filtered_articles = []
    # Her bir makale için...
    for article in articles:
        # Makale başlığını küçük harfe çevir ve kodlamayı çöz
        article_title_decoded, encoding = decode_bytes(article.title.encode('utf-8'))
        # Eğer başlık, herhangi bir anahtar kelimeyi içeriyorsa...
        if any(keyword.lower() in article_title_decoded.lower() for keyword in keywords):
            filtered_articles.append(article)
    return filtered_articles


def calculate_page_range(current_page, total_pages, window=3):
    half_window = window // 2
    start_page = max(current_page - half_window, 1)
    end_page = min(start_page + window - 1, total_pages)

    has_previous = start_page > 1
    has_next = end_page < total_pages
    previous_page = max(current_page - 1, 1)
    next_page = min(current_page + 1, total_pages)

    # range objesini doğrudan döndürmek yerine listeye çevir
    return list(range(start_page, end_page + 1)), has_previous, has_next, previous_page, next_page


def check_user_credentials(username, password):
    correct_username = "admin"
    correct_password = "password"

    # Admin kontrolü
    if username == correct_username and password == correct_password:
        return True, username  # Admin olarak doğrulama

    # Diğer kullanıcılar için kontrol
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)  # Tüm kullanıcıları bir liste olarak yükle
            for user in users:  # Her bir kullanıcı için kontrol et
                if user['username'] == username and user['password'] == password:
                    return True, username  # Kullanıcı doğrulama
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass

    return False, None  # Doğrulama başarısız


