import json
from catansolver.catan import Board, STARTING_RESOURCES
from django.http import HttpResponse
from django.shortcuts import render
from random import shuffle

def home(request):
    return render(request, "home.html", locals())

def new_board(request):
    resources = STARTING_RESOURCES[:]
    shuffle(resources)
    board = Board(resources)
    return HttpResponse(json.dumps(board.to_dict()), mimetype='application/json')
