from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext
from models import Person, Haus, Einladung, Event
from admin import PersonPrivacyForm

def render_to_response(template_name, dictionary=None, context_instance=None, mimetype="text/html", request=None, django=False):
    if django:
        from django.shortcuts import render_to_response
    else:
        from coffin.shortcuts import render_to_response
    global_dictionary = {}
    if dictionary is not None:
        global_dictionary.update(dictionary)
    if context_instance is not None:
        context = context_instance
    else:
        if request is not None:
            context = RequestContext(request)
        else:
            context = None

    #context.update(csrf(request))
    return render_to_response(template_name, global_dictionary, context_instance=context, mimetype=mimetype)

# Create your views here.

def goto(request, hash):
	return redirect('zusage', person_secret=hash)

def zusage(request, person_secret):
    person = get_object_or_404(Person, _secret=person_secret)
    if request.method == 'POST':
        event_id, action = request.POST['ok'].split('_')
        event_id = int(event_id)
        person.toggleEinladung(event_id, action)

    einladungen = []
    for einladung in person.einladung_set.all():
        einladungen.append((einladung.event, einladung.zusage))
    return render_to_response("zusage.html", 
        {'person':person, 'einladungen':person.einladung_set.all()}, request=request)

def privacy(request, person_secret):
    person = get_object_or_404(Person, _secret=person_secret)
    if request.method == 'POST':
        form = PersonPrivacyForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
    else:
        form = PersonPrivacyForm(instance=person)
    return render_to_response("privacy.html", 
        {'person':person, 'form':form}, request=request, django=True)