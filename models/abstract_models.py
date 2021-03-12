from django.db import models
from django_redis_utils.handler import RedisHandler

class RedisCounter(models.Model):
    """
    This class adds a simple 'counter' atribute that keeps, track of how many instances are stored,
    the counter itself its stored on the regular database, but its obtained from redis, that way 
    any instance han unique counter since redis resolves the requests in order working as a buffer.
    """
    
    class Meta:
        abstract = True
    
    #Luego debe ser posible guardar el contador en alguna base de datos,
    #Aunque este campo es bastante universal y funciona en la mayoria
    #de bases de datos.
    counter = models.BigIntegerField(default = 0,null =True)
        
    #Se ejecuta save 2 veces porque se necesita createdDatetime para guardar
    def save(self, *args, **kwargs):
        created = self.pk is not None
        super(RedisCounter, self).save(*args, **kwargs)
        if not created:
            self.after_save()
            super(RedisCounter, self).save(*args, **kwargs)
        
    def after_save(self):
        self.counter = self.incrementar_counter_clase()
    
    def get_varname(self):
        return f"COUNTER_{self.__class__.__name__}"
    
    def incrementar_counter_clase(self):
        return RedisHandler.get_connection().incr(self.get_varname())
    
    def obtener_counter_clase(self):
        valor = RedisHandler.get_connection().get(self.get_varname())
        if valor is not None:
            return valor
        return 0