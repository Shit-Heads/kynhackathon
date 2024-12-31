import json
import requests
from typing import List

API_KEY = "AIzaSyDcQ47Y-SVpFIrSwLFD9eQ0jtqqA-76MC0"
URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
LANGUAGE_CODE = "EN"

def check_fact(query: str) -> List:
    """Search for claims matching the input query text."""
    data = {
        "query": query,
        "pageSize": 25,
        "languageCode": LANGUAGE_CODE,
        "key": API_KEY,
    }

    r = requests.get(URL, params=data)
    rj = r.json()

    claims = rj.get("claims", [])
    results = []

    for c in claims:
        claim_review = c.get("claimReview")[0]
        results.append({
            "claim_text": claim_review.get("title"),
            "claim_conclusion": claim_review.get("textualRating"),
            "claim_url": claim_review.get("url"),
            "claim_date": claim_review.get("reviewDate"),
            "claim_publisher": claim_review.get("publisher").get("name")
        })

    return results

if __name__ == "__main__":
    query = input("Enter the news text to fact-check: ")
    results = check_fact(query)
    if results:
        print(f"Found {len(results)} claims matching your query:")
        for result in results:
            print(f"\nClaim Text: {result['claim_text']}")
            print(f"Conclusion: {result['claim_conclusion']}")
            print(f"Claim URL: {result['claim_url']}")
            print(f"Date: {result['claim_date']}")
            print(f"Publisher: {result['claim_publisher']}")
    else:
        print("No matching claims found.")