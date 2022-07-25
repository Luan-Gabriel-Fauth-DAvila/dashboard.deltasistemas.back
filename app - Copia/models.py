from django.db import models


class GeocodeSearch(models.Model):
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=50)
    cidade = models.CharField(max_length=25)
    pais = models.CharField(max_length=15)
    lat = models.FloatField()
    lon = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cep

    class Meta:
        verbose_name, verbose_name_plural = "GeocodeSearch", "GeocodeSearch"
        ordering = ("cep",)