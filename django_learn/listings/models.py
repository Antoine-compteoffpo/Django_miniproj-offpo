# listings/models.py

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



class Band(models.Model):
    name = models.fields.CharField(max_length=100)  # Champ qui stocke des données de type caractère/texte/chaîne
    class Genre(models.TextChoices): # On définit une nouvelle classe à l'intérieur de la classe précédente
        HIP_HOP = 'HH'
        SYNTH_POP = 'SP'
        ALTERNATIVE_ROCK = 'AR'
    genre = models.fields.CharField(choices=Genre.choices, max_length=5)
    biography = models.fields.CharField(max_length=1000, default='')
    year_formed = models.fields.IntegerField(
    validators=[MinValueValidator(1900), MaxValueValidator(2024)]
    )
    active = models.fields.BooleanField(default=True)
    official_homepage = models.fields.URLField(null=True, blank=True)