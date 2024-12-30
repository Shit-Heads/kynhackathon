import React, { useEffect, useState } from "react";
import axios from "axios";

function NewsFeed() {
    const [news, setNews] = useState([]);

    useEffect(() => {
        axios.get("http://localhost:5000/fetch_news")
            .then(response => setNews(response.data))
            .catch(error => console.error(error));
    }, []);

    return (
        <div>
            <h1>News Feed</h1>
            {news.map((article, index) => (
                <div key={index}>
                    <h2>{article.title}</h2>
                    <p>{article.description}</p>
                    <a href={article.url} target="_blank" rel="noopener noreferrer">Read more</a>
                </div>
            ))}
        </div>
    );
}

export default NewsFeed;
