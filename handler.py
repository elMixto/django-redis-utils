import redis
from django.conf import settings

class RedisHandler():
    """
        Simple class to get a redis connection
    """    
    host = settings.REDIS_HOST
    password = settings.REDIS_PASSWORD
    port = 6379
    db = 1
    
    @classmethod
    def get_connection(cls):
        return redis.Redis(host = cls.host,password=cls.password,port=cls.port,db= cls.db)
    