#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Kapittel
import json

def read_view(request):
	kapitler = Kapittel.objects.all()
	data = {k.pk: k.text for k in kapitler}
	return render(request, 'read.jade', {'kapitler': Kapittel.objects.all(), 'data': json.dumps(data)})
