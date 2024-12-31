from playwright.sync_api import sync_playwright

def scrape_google_news():
    with sync_playwright() as p:
        # Launch a Chromium browser
        browser = p.chromium.launch(headless=False)
        # Open a new page
        page = browser.new_page()
        
        # Navigate to Google News with the search query
        page.goto('https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRE55YXpBU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen')
        
        # Wait for the news articles to load
        page.wait_for_selector('article')

        # Select all article elements
        articles = page.query_selector_all('article')

        # Initialize a list to store news data
        news_data = []

        # Iterate over the first 15 articles
        for article in articles[:3]:  # Limit to 15 articles
            # Extract article details
            headline_element = article.query_selector('.gPFEn')
            source_element = article.query_selector('.vr1PYe')
            image_element = article.query_selector('figure img')
            link_element = article.query_selector('.gPFEn')
            date_element = article.query_selector('time')

            # Retrieve text or attribute values, handling missing elements
            headline = headline_element.inner_text() if headline_element else 'N/A'
            source = source_element.inner_text() if source_element else 'N/A'
            image = image_element.get_attribute('src') if image_element else 'N/A'
            url = link_element.get_attribute('href') if link_element else 'N/A'
            date = date_element.get_attribute('datetime') if date_element else 'N/A'

            # Append the extracted data to the news_data list
            news_data.append({
                'headline': headline,
                'source': source,
                'image': image,
                'url': url,
                'date': date
            })

        # Close the browser
        browser.close()

        # Return the collected news data
        return news_data

if __name__ == '__main__':
    # Scrape Google News for top headlines
    news = scrape_google_news()

    # Print the extracted news articles
    for idx, article in enumerate(news):
        print(f"Article {idx + 1}:")
        print(f"Headline: {article['headline']}")
        print(f"Source: {article['source']}")
        print(f"Date: {article['date']}")
        print(f"Image: https://news.google.com{article['image']}")
        print(f"URL: https://news.google.com{article['url']}")
        print()