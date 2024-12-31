from playwright.sync_api import sync_playwright

def scrape_google_news(location, category):
    search_query = f"{location} {category}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto(f'https://news.google.com/search?q={search_query}')
        page.wait_for_selector('article')

        articles = page.query_selector_all('article')
        news_data = []

        for article in articles[:15]:
            headline_element = article.query_selector('a.JtKRv')
            source_element = article.query_selector('.vr1PYe')
            image_element = article.query_selector('img.Quavad')
            link_element = article.query_selector('a.JtKRv')
            date_element = article.query_selector('time')

            headline = headline_element.inner_text() if headline_element else 'N/A'
            source = source_element.inner_text() if source_element else 'N/A'
            url = f"https://news.google.com{link_element.get_attribute('href')}" if link_element else 'N/A'
            date = date_element.get_attribute('datetime') if date_element else 'N/A'

            image_url = None
            if image_element:
                image_src = image_element.get_attribute('src')
                if image_src:
                    image_url = f"https://news.google.com{image_src}" if not image_src.startswith('http') else image_src
            
            news_data.append({
                'headline': headline,
                'source': source,
                'image_url': image_url,
                'url': url,
                'date': date
            })

        browser.close()
        return news_data

if __name__ == '__main__':
    news = scrape_google_news("mumbai", "f1")
    for article in news:
        print(f"Headline: {article['headline']}")
        print(f"Source: {article['source']}")
        print(f"Date: {article['date']}")
        print(f"URL: {article['url']}")
        print(f"Image URL: {article['image_url']}")
        print()