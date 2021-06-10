from .constants import REDIS_URL
import redis

r = redis.from_url(REDIS_URL)
db_keys = r.keys(pattern='*')
print(len(db_keys))

for key in db_keys:
    chat_id = r.get(key).decode('UTF-8')
    print(key.decode('UTF-8'), ': ', chat_id)
