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
    form = PersonPrivacyForm(instance=person)
    return render_to_response("zusage.html", {'person':person, 'form':form}, request=request)

def zusage2(request, person_secret):
    person = get_object_or_404(Person, _secret=person_secret)
    return render_to_response("zusage_puredjango.html", {'person':person}, request=request, django=True)

privacy = zusage2