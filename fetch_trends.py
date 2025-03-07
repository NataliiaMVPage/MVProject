import feedparser
import json
from datetime import datetime, timezone  # Додано timezone

# 📰 СПИСОК НОВИННИХ САЙТІВ
RSS_FEEDS = {
    "BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "DW (Germany)": "https://rss.dw.com/rdf/rss-en-top",
}

# ФАЙЛ, КУДИ ЗБЕРІГАТИМЕМО НОВИНИ
OUTPUT_FILE = "trends.json"

# 📥 ФУНКЦІЯ ДЛЯ ПАРСИНГУ НОВИН
def fetch_news():
    all_news = []
    
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        news_items = []

        for entry in feed.entries[:10]:  # Беремо 10 останніх новин
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", entry.get("updated", "N/A")),  
                "source": source
            })
        
        all_news.extend(news_items)

    # Додаємо час оновлення (ВИПРАВЛЕНО!)
    result = {
        "updated_at": datetime.now(timezone.utc).isoformat(),  # ✅ Виправлено
        "news": all_news
    }

    # ЗБЕРІГАЄМО В JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"✅ News saved to {OUTPUT_FILE}")

# ЗАПУСКАЄМО СКРИПТ
if __name__ == "__main__":
    fetch_news()