from fastapi import FastAPI, HTTPException
from newspaper import build, Article
import random
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI(title="Random News API")

# List of news websites to fetch from
NEWS_SOURCES = [
    "https://www.bbc.com",
    "https://www.cnn.com",
    "https://www.reuters.com",
    "https://www.theguardian.com"
]

class ArticleResponse(BaseModel):
    title: str
    text: str
    summary: str
    authors: List[str]
    url: str
    source_url: str
    publish_date: str | None

@app.get("/api/random-article", response_model=ArticleResponse)
async def get_random_article():
    try:
        # Randomly select a news source
        source_url = random.choice(NEWS_SOURCES)
        
        # Build newspaper from the source
        paper = build(source_url, memoize_articles=False)
        
        # Get all article URLs
        articles = paper.articles
        
        # Try up to 5 times to get a valid article
        for _ in range(5):
            article = random.choice(articles)
            try:
                article.download()
                article.parse()
                article.nlp()  # This generates the summary
                
                return ArticleResponse(
                    title=article.title,
                    text=article.text,
                    summary=article.summary,
                    authors=article.authors,
                    url=article.url,
                    source_url=source_url,
                    publish_date=str(article.publish_date) if article.publish_date else None
                )
            except Exception:
                continue
                
        raise HTTPException(status_code=500, detail="Failed to fetch a valid article")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to Random News API. Use /api/random-article to get a random news article."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)