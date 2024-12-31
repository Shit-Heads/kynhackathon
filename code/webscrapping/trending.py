from playwright.sync_api import sync_playwright
import time

def scrape_trending_news(category):
    search_term = f"trending {category} news"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto('https://www.bing.com/news')
        page.fill('input[name="q"]', search_term)
        page.press('input[name="q"]', 'Enter')
        
        page.wait_for_selector('.news-card', timeout=10000)
        time.sleep(2)
        
        articles = page.query_selector_all('.news-card')
        news_data = []
        
        for article in articles[:2]:
            try:
                # Extract title and link
                title_element = article.query_selector('.title')
                title = title_element.inner_text() if title_element else 'N/A'
                link = title_element.get_attribute('href') if title_element else 'N/A'
                
                # Extract source and time
                source_element = article.query_selector('.source')
                source = source_element.inner_text() if source_element else 'N/A'
                time_element = article.query_selector('time')
                published = time_element.inner_text() if time_element else 'N/A'
                
                # Extract description
                description_element = article.query_selector('.snippet')
                description = description_element.inner_text() if description_element else 'N/A'
                
                # Extract image
                img_element = article.query_selector('img')
                if img_element:
                    image_url = img_element.get_attribute('src')
                    # If src is not available, try data-src
                    if not image_url:
                        image_url = img_element.get_attribute('data-src')
                else:
                    image_url = 'N/A'
                
                news_data.append({
                    'title': title,
                    'link': link,
                    'source': source,
                    'published': published,
                    'description': description,
                    'image_url': image_url
                })
            except Exception as e:
                print(f"Error processing article: {e}")
                continue
        
        browser.close()
        return news_data

if __name__ == "__main__":
    results = scrape_trending_news("technology")
    print(results)
    # for article in results:
    #     print("\n---Article---")
    #     print(f"Title: {article['title']}")
    #     print(f"Source: {article['source']}")
    #     print(f"Published: {article['published']}")
    #     print(f"Link: {article['link']}")
    #     print(f"Description: {article['description']}")
    #     print(f"Image URL: {article['image_url']}")