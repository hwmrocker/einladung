from einladung.models import Person, Haus, Event, Einladung

from django.contrib import admin
from django import forms

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person

class PersonPrivacyForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ("handy", "handy_erreichbar", "handy_sichtbar", "festnetz", "festnetz_erreichbar",
            "festnetz_sichtbar", "anschrift", "anschrift_sichtbar")

class EventAdminForm(forms.ModelForm):
    mm = forms.ModelMultipleChoiceField(
        queryset=Person.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple("Foo", False, attrs={'rows':'10'}))

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['mm'] = [t.service.pk for t in kwargs['instance'].event_person_set.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, commit)

        old_save_m2m = self.save_m2m
        def save_m2m():
            old_save_m2m()

            messages = [s for s in self.cleaned_data['ss']]
            for mf in instance.message_forum_set.all():
                if mf.service not in messages:
                    mf.delete()
                else:
                    messages.remove(mf.service)

            for message in messages:
                Message_forum.objects.create(message=message, forum=instance)

        self.save_m2m = save_m2m

        return instance

    class Meta:
        model = Event

class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm

admin.site.register(Person)
admin.site.register(Haus)
admin.site.register(Event)
admin.site.register(Einladung)