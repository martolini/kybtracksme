#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from kybsal.contact.models import Improvement
from kybsal.contact.forms import ImprovementForm
from django.contrib import messages


@login_required
def contact(request):
	clean_form = ImprovementForm(initial={'sender': request.user.username})
	if request.method == 'POST':
		form = ImprovementForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Takk. Dette blir sjekka opp så fort som mulig!")
			return render(request, 'kontakt.jade', {'form': clean_form} )
		messages.error(request, "Kunne ikke sende.")

	return render(request, 'kontakt.jade', {'form':clean_form})
