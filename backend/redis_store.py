import redis

class RedisStore:
    def __init__(self, url):
        self.redis = redis.from_url(url)
    
    def get_data(self, key):
        value = self.redis.get(key)
        return value.decode() if value else None
    
    def set_data(self, key, value):
        self.redis.set(key, value)

# Replace 'redis://localhost:6379' with your actual Redis URL
store = RedisStore('redis://localhost:6379')