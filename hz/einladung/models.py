#encoding: UTF-8
from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import random
import string

SECERETS = string.digits + string.lowercase

class Event(models.Model):
    name = models.CharField(max_length=60)
    ort = models.TextField(null=True, blank=True)
    datum = models.DateTimeField()
    _html_class = models.CharField(max_length=30, null=True, blank=True)
    # http://stackoverflow.com/questions/2854350/django-admin-many-to-many-listbox-doesnt-show-up-with-a-through-parameter
    personen = models.ManyToManyField('Person', through='Einladung', blank=True)

    def __unicode__(self):
        return self.name

class Einladung(models.Model):
    person = models.ForeignKey('Person') 
    event = models.ForeignKey('Event')
    ZUSAGE = (
        ('-', 'Unbekannt'),
        ('Z', 'Zusage'),
        ('A', 'Absage'),
    )    
    zusage = models.CharField(max_length=1, choices=ZUSAGE, default='-')
    def __unicode__(self):
        return "%s - %s" % (self.event, self.person)

class PersonenManager(models.Manager):
    use_for_related_fields = True

    def bietenSchlafplaetze(self):
        return self.get_query_set().filter()
        
class Person(models.Model):
    user = models.OneToOneField(User)
    objects = PersonenManager()
    # TODO: if name or email is accessed or edited user.name or user.email is used instead
    name = models.CharField(max_length=60, null=True, blank=True)
    SICHTBAR = (
        ('B', 'Brautpaar, evtl Helfer'),
        ('S', 'Schlafplatzsuchende'),
        ('L', 'Alle mit Login'),
        ('A', 'Alle'),
    )
    email = models.EmailField()
    email_sichtbar = models.CharField(max_length=1, choices=SICHTBAR, default='B')
    handy = models.CharField(max_length=40, null=True, blank=True)
    handy_sichtbar = models.CharField(max_length=1, choices=SICHTBAR, default='B')
    handy_erreichbar = models.CharField(max_length=100, null=True, blank=True)
    festnetz = models.CharField(max_length=40, null=True, blank=True)
    festnetz_sichtbar = models.CharField(max_length=1, choices=SICHTBAR, default='B')
    festnetz_erreichbar = models.CharField(max_length=100, null=True, blank=True)
    anschrift = models.TextField(max_length=100, null=True, blank=True)
    anschrift_sichtbar = models.CharField(max_length=1, choices=SICHTBAR, default='B')

    SUCHE_BETT = (
        ('-', 'Keine Schlafmöglichkeit'),
        ('B', 'Bett'),
        ('C', 'Couch'),
        ('_', 'Boden'),
    )
    suche = models.CharField(max_length=1, choices=SUCHE_BETT, default='-')

    bewerbungSchlafplatz = models.ForeignKey('Haus', null=True, blank=True)
    _zusage_fuer_bett = models.ForeignKey('Haus', related_name='zusageBett', null=True, blank=True)
    _zusage_fuer_couch = models.ForeignKey('Haus', related_name='zusageCouch', null=True, blank=True)
    _zusage_fuer_boden = models.ForeignKey('Haus', related_name='zusageBoden', null=True, blank=True)
    
    _secret = models.CharField(max_length=2, unique=True, 
        default=lambda: "".join([random.choice(SECERETS) for r in range(2)]))
    _pack = models.CharField(max_length=60, blank=True, default='')
    einladung_gelesen = models.BooleanField()

    def __unicode__(self):
        return "%s (%d)[%s]" % (self.user.username, self.pk, self._secret)

    def toggleEinladung(self, event_id, action):
        einladung = self.einladung_set.get(event_id=event_id)
        action = action.upper()
        assert action in ('Z', 'A')
        if einladung.zusage == action:
            einladung.zusage = '-'
        else:
            einladung.zusage = action
        einladung.save()

    def getPack(self):
        return Person.objects.filter(_pack=self._pack).all()

    def getOthers(self):
        return Person.objects.filter(_pack=self._pack).exclude(pk=self.pk).all()


class Haus(models.Model):
    kontakperson = models.ForeignKey('Person')
    anschrift = models.TextField()

    bieteBett = models.SmallIntegerField()
    bieteCouch = models.SmallIntegerField()
    bieteBoden = models.SmallIntegerField()

    #TODO für Event

    
