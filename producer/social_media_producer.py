
import os
import json
import time
import logging
from kafka import KafkaProducer
import tweepy
from dotenv import load\_dotenv

logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(**name**)

load\_dotenv()

bearer\_token = os.getenv('SOCIAL\_MEDIA\_BEARER\_TOKEN')
if not bearer\_token:
logger.error("SOCIAL\_MEDIA\_BEARER\_TOKEN not set")
raise ValueError("SOCIAL\_MEDIA\_BEARER\_TOKEN environment variable not set")

bootstrap\_servers = os.getenv('KAFKA\_BOOTSTRAP\_SERVERS', 'kafka:9093')
topic\_name = os.getenv('KAFKA\_TOPIC', 'social\_media\_posts')

class SocialMediaProducer:
def **init**(self):
self.producer = KafkaProducer(
bootstrap\_servers=bootstrap\_servers,
value\_serializer=lambda v: json.dumps(v).encode('utf-8'),
security\_protocol=os.getenv('KAFKA\_SECURITY\_PROTOCOL', 'SASL\_SSL'),
sasl\_mechanism=os.getenv('KAFKA\_SASL\_MECHANISM', 'PLAIN'),
sasl\_plain\_username=os.getenv('KAFKA\_CLIENT\_USER'),
sasl\_plain\_password=os.getenv('KAFKA\_CLIENT\_PASSWORD')
)
self.client = tweepy.Client(bearer\_token=bearer\_token)
self.keywords = \["AI", "machine learning", "data science", "technology", "python"]
logger.info("Social Media Producer initialized")

```
def fetch_and_send_tweets(self):
    try:
        for keyword in self.keywords:
            tweets = self.client.search_recent_tweets(
                query=keyword,
                max_results=10,
                tweet_fields=["created_at", "lang", "text"]
            )
            if not tweets.data:
                logger.warning(f"No tweets for {keyword}")
                continue
            for t in tweets.data:
                if t.lang == 'en':
                    data = {
                        'id': str(t.id),
                        'text': t.text,
                        'created_at': t.created_at.isoformat(),
                        'keyword': keyword
                    }
                    self.producer.send(topic_name, data)
                    logger.info(f"Sent tweet {t.id}")
            time.sleep(5)
    except Exception as e:
        logger.error(f"Fetch error: {e}")

def run(self):
    logger.info(f"Producing to {topic_name}")
    try:
        while True:
            self.fetch_and_send_tweets()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Interrupted")
    finally:
        self.producer.close()
```

if **name** == '**main**':
time.sleep(30)
SocialMediaProducer().run()


