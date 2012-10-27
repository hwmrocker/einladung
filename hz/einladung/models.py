#encoding: UTF-8
from django.db import models
from django.contrib.auth.models import User

class PollManager(models.Manager):
    use_for_related_fields = True
    def zusageEssen(self):
        return self.get_query_set().filter(EssenEinladung=True).filter(EssenZusage="Z")
    def zusageKirche(self):
        return self.get_query_set().filter(KircheEinladung=True).filter(KircheZusage="Z")
    def zusageFeier(self):
        return self.get_query_set().filter(FeierEinladung=True).filter(FeierZusage="Z")
    def bietenSchlafplaetze(self):
        return self.get_query_set().filter()
        
class Person(models.Model):
    user = models.OneToOneField(User)
    objects = PollManager()
    #name = models.CharField()
    #email = models.EmailField()
    SICHTBAR = (
        ('B', 'Brautpaar, evtl Helfer'),
        ('S', 'Schlafplatzsuchende'),
        ('L', 'Alle mit Login'),
        ('A', 'Alle'),
    )
    handy = models.CharField(max_length=40, null=True, blank=True)
    handy_erreichbar = models.CharField(max_length=100, null=True, blank=True)
    handy_sichtbar = models.CharField(max_length=1, choices=SICHTBAR, default='B', null=True, blank=True)
    festnetz = models.CharField(max_length=40, null=True, blank=True)
    festnetz_erreichbar = models.CharField(max_length=100, null=True, blank=True)
    festnetz_sichtbar = models.CharField(max_length=1, choices=SICHTBAR, default='B', null=True, blank=True)
    anschrift = models.TextField(max_length=100, null=True, blank=True)
    anschrift_sichtbar = models.CharField(max_length=1, choices=SICHTBAR, default='B', null=True, blank=True)

    KircheEinladung = models.BooleanField()
    EssenEinladung = models.BooleanField()
    FeierEinladung = models.BooleanField()
    JunggesellenAbschiedEinladung = models.BooleanField()
    JungesellinenAbschiedEinladung = models.BooleanField()
    PolterabendEinladung = models.BooleanField()

    ZUSAGE = (
        ('-', 'Unbekannt'),
        ('Z', 'Zusage'),
        ('A', 'Absage'),
    )
    KircheZusage = models.CharField(max_length=1, choices=ZUSAGE, default='-')
    EssenZusage = models.CharField(max_length=1, choices=ZUSAGE, default='-')
    FeierZusage = models.CharField(max_length=1, choices=ZUSAGE, default='-')
    JunggesellenAbschiedZusage = models.CharField(max_length=1, choices=ZUSAGE, default='-')
    JungesellinenAbschiedZusage = models.CharField(max_length=1, choices=ZUSAGE, default='-')
    PolterabendZusage = models.CharField(max_length=1, choices=ZUSAGE, default='-')

    SUCHE_BETT = (
        ('-', 'Keine Schlafmöglichkeit'),
        ('B', 'Bett'),
        ('C', 'Couch'),
        ('_', 'Boden'),
    )
    suche = models.CharField(max_length=1, choices=SUCHE_BETT, default='-')
    #sucheBett = models.BooleanField()
    #sucheCouch = models.BooleanField()
    #sucheBoden = models.BooleanField()

    bewerbungSchlafplatz = models.ForeignKey('Haus', null=True, blank=True)
    _zusage_fuer_bett = models.ForeignKey('Haus', related_name='zusageBett', null=True, blank=True)
    _zusage_fuer_couch = models.ForeignKey('Haus', related_name='zusageCouch', null=True, blank=True)
    _zusage_fuer_boden = models.ForeignKey('Haus', related_name='zusageBoden', null=True, blank=True)
    

    einladung_gelesen = models.BooleanField()

class Haus(models.Model):
    kontakperson = models.ForeignKey('Person')
    anschrift = models.TextField()

    bieteBett = models.SmallIntegerField()
    bieteCouch = models.SmallIntegerField()
    bieteBoden = models.SmallIntegerField()

    
