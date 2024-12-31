from playwright.sync_api import sync_playwright

def scrape_google_news(location, category):
    search_query = f"{location} {category}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to Google News with the search query
        page.goto(f'https://news.google.com/search?q={search_query}')
        
        # Wait for the news articles to load
        page.wait_for_selector('article')

        articles = page.query_selector_all('article')

        news_data = []

        for article in articles[:15]:  # Limit to 15 articles
            headline_element = article.query_selector('a.JtKRv')
            source_element = article.query_selector('.vr1PYe')
            image_element = article.query_selector('.Quavad')
            link_element = article.query_selector('a.JtKRv')
            date_element = article.query_selector('time')

            headline = headline_element.inner_text() if headline_element else 'N/A'
            source = source_element.inner_text() if source_element else 'N/A'
            image = image_element.get_attribute('src') if image_element else 'N/A'
            url = link_element.get_attribute('href') if link_element else 'N/A'
            date = date_element.get_attribute('datetime') if date_element else 'N/A'

            news_data.append({
                'headline': headline,
                'source': source,
                'image': image,
                'url': url,
                'date': date
            })

        browser.close()
        return news_data

if __name__ == '__main__':
    location = input("Enter Location: ")
    category = input("Enter Category: ")
    news = scrape_google_news(location, category)
    print(news)
    # for idx, article in enumerate(news):
    #     print(f"Article {idx + 1}:")
    #     print(f"Headline: {article['headline']}")
    #     print(f"Source: {article['source']}")
    #     print(f"Date: {article['date']}")
    #     print(f"Image: https://news.google.com{article['image']}")
    #     print(f"URL: https://news.google.com{article['url']}")
    #     print()